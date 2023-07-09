#include <prometheus/counter.h>
#include <prometheus/exposer.h>
#include <prometheus/registry.h>

#include <thread>
#include <chrono>

int main() {
    // Create a Prometheus registry.
    auto registry = std::make_shared<prometheus::Registry>();

    // Create a counter.
    auto& counter_family = prometheus::BuildCounter()
        .Name("app_requests_total")
        .Help("Total app requests")
        .Register(*registry);
    auto& counter = counter_family.Add({});

    // Increment the counter.
    counter.Increment();

    // Expose the metrics.
    prometheus::Exposer exposer{"127.0.0.1:8001"};
    exposer.RegisterCollectable(registry);

    // Add an infinite loop to keep the program running.
    for (;;) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
