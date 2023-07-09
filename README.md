# prometheus-test
C++ with prometheus


1. Compile and run the C++ application:

Navigate to your C++ project directory and run these commands:
```bash
mkdir build
cd build
cmake ..
make
./MyProject
```

This will start your C++ application, and it will start exposing metrics at http://127.0.0.1:8001/metrics.


2. Run the Python application:
```bash
python3 server.py
```

Ensure your Python script is running and exposing metrics at http://127.0.0.1:8000.


3. Run Prometheus:
Download and unzip prometheus from:
https://prometheus.io/download/

3. Start the Prometheus server with the configuration file:
Example:
~/Downloads/prometheus-2.45.0.darwin-amd64/prometheus --config.file=prometheus.yml

4. Check the Prometheus UI:
Open a web browser and go to http://127.0.0.1:9090.

Click on "Graph" from the top menu, then choose "Console" below. In the "Expression" input box, type app_requests_total (or whatever metric you're collecting), then click "Execute". You should see the metric values from both your Python and C++ applications.
