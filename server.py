import json
import os
import signal
import socket
import time
import logging
import stat
import selectors
from prometheus_client import Gauge, start_http_server

# Define Prometheus metrics
TEST_GAUGE = Gauge('test_gauge', 'A gauge for testing.', ['name'])

class MetricsServer:
    """A server that listens for metrics on a Unix domain socket."""

    def __init__(self, socket_path, listen_backlog=1):
        self.socket_path = socket_path
        self.listen_backlog = listen_backlog
        self.running = True
        self.selector = selectors.DefaultSelector()

    def start(self):
        """Start the server."""
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(self.socket_path)
        # Set socket file permissions to rw------- for security
        os.chmod(self.socket_path, stat.S_IRUSR | stat.S_IWUSR)
        s.listen(self.listen_backlog)
        s.setblocking(False)
        self.selector.register(s, selectors.EVENT_READ)

        while self.running:
            events = self.selector.select(timeout=1)
            for key, mask in events:
                conn, addr = key.fileobj.accept()
                with conn:
                    self._read_metrics(conn)
            time.sleep(5)
            
        self.selector.unregister(s)
        s.close()

    def stop(self):
        """Stop the server."""
        self.running = False
        self.cleanup()

    def _read_metrics(self, conn):
        """Read metrics from the Unix domain socket.

        Args:
            conn: A socket connection object.
        """
        try:
            data = conn.recv(1024).decode()
            json_data = json.loads(data)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logging.error(f"Failed to parse data: {e}")
            return

        logging.info(json_data)

        if 'gauge' in json_data and isinstance(json_data['gauge'], int) and \
            'name' in json_data and isinstance(json_data['name'], str):
            TEST_GAUGE.labels(name=json_data.get('name', 'unknown')).set(
                json_data['gauge'])

    def cleanup(self):
        """Clean up resources."""
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)


def setup_logging():
    """Set up basic logging configuration."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    setup_logging()

    # Start the server to expose the metrics.
    start_http_server(8001)

    server = MetricsServer('/tmp/metrics.sock')

    def signal_handler(signal, frame):
        logging.info("Received exit signal. Cleaning up...")
        server.stop()
    
    # Set up signal handling for SIGINT
    signal.signal(signal.SIGINT, signal_handler)
    
    server.start()
