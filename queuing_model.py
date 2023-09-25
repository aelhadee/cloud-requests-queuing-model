import numpy as np
import matplotlib.pyplot as plt

def simulate_queue(arrival_rate, service_rate, num_servers, num_requests):
    interarrival_times = np.random.exponential(1/arrival_rate, num_requests)
    service_times = np.random.exponential(1/service_rate, num_requests)
    
    arrival_times = [0]
    departure_times = []
    
    for i in range(num_requests):
        arrival_times.append(arrival_times[-1] + interarrival_times[i])
        
        if i < num_servers or departure_times[i-num_servers] < arrival_times[i]:
            departure_times.append(arrival_times[i] + service_times[i])
        else:
            departure_times.append(departure_times[i-1] + service_times[i])
    
    waiting_times = np.array(departure_times) - np.array(arrival_times[:-1])
    return waiting_times

# Set parameters
arrival_rate = 10_000
service_rate_traditional = 100
service_rate_ndn = 500
num_servers = 20
num_requests_range = np.linspace(1_000, 10_000, 10)

avg_waiting_times_traditional = []
avg_waiting_times_ndn = []

# Simulate for each number of requests and compute average waiting times
for num_requests in num_requests_range:
    waiting_times_traditional = simulate_queue(arrival_rate, service_rate_traditional, num_servers, int(num_requests))
    waiting_times_ndn = simulate_queue(arrival_rate, service_rate_ndn, num_servers, int(num_requests))
    avg_waiting_times_traditional.append(np.mean(waiting_times_traditional))
    avg_waiting_times_ndn.append(np.mean(waiting_times_ndn))

# Plot average waiting times
plt.figure()
plt.plot(num_requests_range, avg_waiting_times_traditional, label='Traditional')
plt.plot(num_requests_range, avg_waiting_times_ndn, label='NDN')
plt.xlabel('Number of Requests')
plt.ylabel('Average Waiting Time (seconds)')
plt.title('Average Waiting Time')
plt.legend()
plt.grid(True)
plt.show()

# Histogram and CDF of Waiting Times for the maximum number of requests
waiting_times_traditional = simulate_queue(arrival_rate, service_rate_traditional, num_servers, int(num_requests_range[-1]))
waiting_times_ndn = simulate_queue(arrival_rate, service_rate_ndn, num_servers, int(num_requests_range[-1]))

plt.figure()
plt.hist(waiting_times_traditional, bins=500, alpha=0.5, label='Traditional', density=True)
plt.hist(waiting_times_ndn, bins=500, alpha=0.5, label='NDN', density=True)
plt.xlabel('Waiting Time (seconds)')
plt.ylabel('Probability Density')
plt.title('Histogram of Waiting Times')
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
plt.hist(waiting_times_traditional, bins=1000, alpha=0.5, label='Traditional', density=True, cumulative=True)
plt.hist(waiting_times_ndn, bins=1000, alpha=0.5, label='NDN', density=True, cumulative=True)
plt.xlabel('Waiting Time (seconds)')
plt.ylabel('CDF')
plt.title('CDF of Waiting Times')
plt.legend()
plt.grid(True)
plt.show()
