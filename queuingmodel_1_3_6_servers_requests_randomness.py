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
arrival_rate = 1000
service_rate_traditional = 10
service_rate_ndn = 15
server_counts = [1, 3, 6]  # Now including 1 server
num_simulations = 100
request_lower_bound = 100
request_upper_bound = 1000

# Data preparation for scatter plot (average waiting times) and CDF plot
scatter_data = {num_servers: {'Traditional': [], 'NDN': []} for num_servers in server_counts}
aggregated_waiting_times = {num_servers: {'Traditional': [], 'NDN': []} for num_servers in server_counts}

for num_servers in server_counts:
    for _ in range(num_simulations):
        num_requests = np.random.randint(request_lower_bound, request_upper_bound)
        scatter_data[num_servers]['Traditional'].append(
            (num_requests, np.mean(simulate_queue(arrival_rate, service_rate_traditional, num_servers, num_requests))))
        scatter_data[num_servers]['NDN'].append(
            (num_requests, np.mean(simulate_queue(arrival_rate, service_rate_ndn, num_servers, num_requests))))
        # Aggregating waiting times for CDF plot
        aggregated_waiting_times[num_servers]['Traditional'].extend(simulate_queue(arrival_rate, service_rate_traditional, num_servers, num_requests))
        aggregated_waiting_times[num_servers]['NDN'].extend(simulate_queue(arrival_rate, service_rate_ndn, num_servers, num_requests))

# Scatter plot for average waiting times vs. number of requests
plt.figure(figsize=(12, 8))
colors_line = ['skyblue', 'navy', 'lightgreen', 'darkgreen', 'red', 'purple']  # Updated colors for 1, 3, and 6 servers

i = 0  # Color index
for num_servers in server_counts:
    for config in ['Traditional', 'NDN']:
        sorted_data = sorted(scatter_data[num_servers][config], key=lambda x: x[0])
        requests, waiting_times = zip(*sorted_data)
        plt.plot(requests, waiting_times, label=f'{config} {num_servers} servers', color=colors_line[i], linestyle='--' if config == 'NDN' else '-')
        i += 1

plt.xlabel('Number of Requests')
plt.ylabel('Average Waiting Time (seconds)')
plt.title('Average Waiting Time vs. Number of Requests with Randomness')
plt.legend()
plt.grid(True)
plt.show()

# CDF plot for aggregated waiting times
plt.figure(figsize=(12, 8))
i = 0  # Reset color index for CDF plot
for num_servers in server_counts:
    for config in ['Traditional', 'NDN']:
        waiting_times = aggregated_waiting_times[num_servers][config]
        sorted_times = np.sort(waiting_times)
        cdf = np.arange(1, len(sorted_times) + 1) / len(sorted_times)
        plt.plot(sorted_times, cdf, label=f'{config} {num_servers} servers', color=colors_line[i], linestyle='--' if config == 'NDN' else '-')
        i += 1

plt.xlabel('Waiting Time (seconds)')
plt.ylabel('CDF')
plt.title('Aggregated CDF of Waiting Times for Traditional vs. NDN Servers')
plt.legend()
plt.grid(True)
plt.show()

# Box plot for actual waiting times
plt.figure(figsize=(12, 8))
box_plot_data = []
labels = []

for num_servers in server_counts:
    for config in ['Traditional', 'NDN']:
        waiting_times = aggregated_waiting_times[num_servers][config]
        box_plot_data.append(waiting_times)
        labels.append(f'{config} {num_servers} servers')

plt.boxplot(box_plot_data, labels=labels, patch_artist=True)
plt.xticks(rotation=45)
plt.ylabel('Waiting Times (seconds)')
plt.title('Distribution of Waiting Times Across Server Configurations')
plt.grid(True)
plt.show()
