#include <boost/asio.hpp>
#include <iostream>
#include <nlohmann/json.hpp>
#include <string>

using boost::asio::local::stream_protocol;
using json = nlohmann::json;
using std::cerr;
using std::exception;
using std::string;

constexpr char kSocketPath[] = "/tmp/metrics.sock";

void send_metrics() {
    try {
        boost::asio::io_service io_service;

        // Connect to the Unix domain socket
        stream_protocol::socket s(io_service);
        s.connect(stream_protocol::endpoint(kSocketPath));

        // Create a complex JSON object
        json data{{"name", "test"}, {"gauge", 10}};

        // Convert the JSON to a string and send it to the Python server
        string message = data.dump() + "\n";
        boost::asio::write(s, boost::asio::buffer(message));
    } catch (exception& e) {
        cerr << "Exception: " << e.what() << "\n";
    }
}

int main() {
    send_metrics();
    return 0;
}
