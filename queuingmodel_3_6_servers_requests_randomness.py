import numpy as np
import matplotlib.pyplot as plt

def simulate_queue(arrival_rate, service_rate, num_servers, num_requests):
    interarrival_times = np.random.exponential(1/arrival_rate, num_requests)
    service_times = np.random.exponential(1/service_rate, num_requests)
    
    arrival_times = np.cumsum(interarrival_times)
    departure_times = [0] * num_requests
    servers_free_time = [0] * num_servers
    
    for i in range(num_requests):
        earliest_free_server_time = min(servers_free_time)
        if arrival_times[i] < earliest_free_server_time:
            departure_times[i] = earliest_free_server_time + service_times[i]
        else:
            departure_times[i] = arrival_times[i] + service_times[i]
        
        server_index = servers_free_time.index(earliest_free_server_time)
        servers_free_time[server_index] = departure_times[i]
    
    waiting_times = [dep - arr for dep, arr in zip(departure_times, arrival_times)]
    return waiting_times

# Parameters
arrival_rate = 10_000
service_rate_traditional = 100
service_rate_ndn = 150
server_counts = [3, 6]
num_simulations = 100
request_lower_bound = 1_000
request_upper_bound = 10_000
num_scenarios = 10

# Scatter plot data preparation
scatter_data = {num_servers: {'Traditional': [], 'NDN': []} for num_servers in server_counts}

for num_servers in server_counts:
    for _ in range(num_simulations):
        num_requests = np.random.randint(request_lower_bound, request_upper_bound)
        scatter_data[num_servers]['Traditional'].append(
            (num_requests, np.mean(simulate_queue(arrival_rate, service_rate_traditional, num_servers, num_requests))))
        scatter_data[num_servers]['NDN'].append(
            (num_requests, np.mean(simulate_queue(arrival_rate, service_rate_ndn, num_servers, num_requests))))

# CDF data aggregation
aggregated_waiting_times = {num_servers: {'Traditional': [], 'NDN': []} for num_servers in server_counts}

for num_servers in server_counts:
    for _ in range(num_scenarios):
        num_requests = np.random.randint(request_lower_bound, request_upper_bound)
        aggregated_waiting_times[num_servers]['Traditional'].extend(simulate_queue(arrival_rate, service_rate_traditional, num_servers, num_requests))
        aggregated_waiting_times[num_servers]['NDN'].extend(simulate_queue(arrival_rate, service_rate_ndn, num_servers, num_requests))

# Plotting
# Line plot for average waiting times vs. number of requests
plt.figure(figsize=(12, 8))
colors_line = ['skyblue', 'navy', 'lightgreen', 'darkgreen']  # Colors for each configuration and server count

for idx, num_servers in enumerate(server_counts):
    traditional_sorted = sorted(scatter_data[num_servers]['Traditional'], key=lambda x: x[0])
    traditional_requests, traditional_waiting = zip(*traditional_sorted)
    plt.plot(traditional_requests, traditional_waiting, label=f'Traditional {num_servers} servers', color=colors_line[idx * 2])

    ndn_sorted = sorted(scatter_data[num_servers]['NDN'], key=lambda x: x[0])
    ndn_requests, ndn_waiting = zip(*ndn_sorted)
    plt.plot(ndn_requests, ndn_waiting, label=f'NDN {num_servers} servers', color=colors_line[idx * 2 + 1], linestyle='--')

plt.xlabel('Number of Requests')
plt.ylabel('Average Waiting Time (seconds)')
plt.title('Average Waiting Time vs. Number of Requests with Randomness')
plt.legend()
plt.grid(True)
plt.show()

# CDF plot for aggregated waiting times
plt.figure(figsize=(12, 8))
for idx, num_servers in enumerate(server_counts):
    sorted_traditional = np.sort(aggregated_waiting_times[num_servers]['Traditional'])
    cdf_traditional = np.arange(1, len(sorted_traditional) + 1) / len(sorted_traditional)
    plt.plot(sorted_traditional, cdf_traditional, label=f'Traditional {num_servers} servers', color=colors_line[idx * 2])
    
    sorted_ndn = np.sort(aggregated_waiting_times[num_servers]['NDN'])
    cdf_ndn = np.arange(1, len(sorted_ndn) + 1) / len(sorted_ndn)
    plt.plot(sorted_ndn, cdf_ndn, '--', label=f'NDN {num_servers} servers', color=colors_line[idx * 2 + 1])

plt.xlabel('Waiting Time (seconds)')
plt.ylabel('CDF')
plt.title('Aggregated CDF of Waiting Times for Traditional vs. NDN Servers')
plt.legend()
plt.grid(True)
plt.show()
