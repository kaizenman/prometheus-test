from prometheus_client import start_http_server, Counter
import time

# Create a counter metric.
request_count = Counter('app_requests_total', 'Total app requests')

# Function to increment the counter.
def handle_request(request):
    # Increment the counter.
    request_count.inc()

    # Handle the request here...

# Start the server to expose the metrics.
start_http_server(8000)

# Your application logic here...

# Add an infinite loop to keep the program running.
while True:
    time.sleep(1)
