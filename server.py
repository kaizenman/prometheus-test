import json
import os
import socket
import time
from prometheus_client import Gauge, start_http_server

# Define Prometheus metrics
TEST_GAUGE = Gauge('test_gauge',
                   'A counter for testing.',
                   ['name'])

# Path for Unix domain socket
SOCK_PATH = '/tmp/metrics.sock'


def read_metrics(sock):
    """Read metrics from the Unix domain socket.

    Args:
        sock: A socket connection object.
    """
    data = sock.recv(1024).decode()
    json_data = json.loads(data)
    print(json_data)

    if 'gauge' in json_data:
        TEST_GAUGE.labels(name=json_data.get('name', 'unknown')).set(
            json_data['gauge'])


def create_socket_and_listen():
    """Create a Unix domain socket and listen for metrics."""
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        s.bind(SOCK_PATH)
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                read_metrics(conn)
            time.sleep(5)
    finally:
        s.close()
        os.remove(SOCK_PATH)


if __name__ == '__main__':
    # Start the server to expose the metrics.
    start_http_server(8001)
    create_socket_and_listen()
