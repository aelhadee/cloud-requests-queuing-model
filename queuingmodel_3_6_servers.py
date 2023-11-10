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
            # Wait for the earliest server to be free
            departure_times[i] = earliest_free_server_time + service_times[i]
        else:
            # Immediately process the request as there's a free server
            departure_times[i] = arrival_times[i] + service_times[i]
        
        # Update the time the server will be free next
        server_index = servers_free_time.index(earliest_free_server_time)
        servers_free_time[server_index] = departure_times[i]
    
    waiting_times = [dep - arr for dep, arr in zip(departure_times, arrival_times)]
    return waiting_times

# Set parameters
arrival_rate = 10_000
service_rate_traditional = 100
service_rate_ndn = 150
server_counts = [3, 6]
num_requests_range = np.linspace(1_000, 10_000, 10)

plt.figure()
for num_servers in server_counts:
    avg_waiting_times_traditional = []
    avg_waiting_times_ndn = []
    for num_requests in num_requests_range:
        waiting_times_traditional = simulate_queue(arrival_rate, service_rate_traditional, num_servers, int(num_requests))
        waiting_times_ndn = simulate_queue(arrival_rate, service_rate_ndn, num_servers, int(num_requests))
        avg_waiting_times_traditional.append(np.mean(waiting_times_traditional))
        avg_waiting_times_ndn.append(np.mean(waiting_times_ndn))

    plt.plot(num_requests_range, avg_waiting_times_traditional, label=f'Traditional {num_servers} servers')
    plt.plot(num_requests_range, avg_waiting_times_ndn, label=f'NDN {num_servers} servers', linestyle='--')

plt.xlabel('Number of Requests')
plt.ylabel('Average Waiting Time (seconds)')
plt.title('Average Waiting Time vs. Number of Requests')
plt.legend()
plt.grid(True)
plt.show()

# Overlay histogram and CDF plots for all server counts
plt.figure()
for num_servers in server_counts:
    waiting_times_traditional = simulate_queue(arrival_rate, service_rate_traditional, num_servers, int(num_requests_range[-1]))
    waiting_times_ndn = simulate_queue(arrival_rate, service_rate_ndn, num_servers, int(num_requests_range[-1]))
    
    plt.hist(waiting_times_traditional, bins=500, alpha=0.5, label=f'Traditional {num_servers} servers', density=True, histtype='step')
    plt.hist(waiting_times_ndn, bins=500, alpha=0.5, label=f'NDN {num_servers} servers', linestyle='--', density=True, histtype='step')

plt.xlabel('Waiting Time (seconds)')
plt.ylabel('Probability Density')
plt.title('Histogram of Waiting Times')
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
for num_servers in server_counts:
    waiting_times_traditional = simulate_queue(arrival_rate, service_rate_traditional, num_servers, int(num_requests_range[-1]))
    waiting_times_ndn = simulate_queue(arrival_rate, service_rate_ndn, num_servers, int(num_requests_range[-1]))
    
    plt.hist(waiting_times_traditional, bins=1000, alpha=0.5, label=f'Traditional {num_servers} servers', density=True, cumulative=True, histtype='step')
    plt.hist(waiting_times_ndn, bins=1000, alpha=0.5, label=f'NDN {num_servers} servers', linestyle='--', density=True, cumulative=True, histtype='step')

plt.xlabel('Waiting Time (seconds)')
plt.ylabel('CDF')
plt.title('CDF of Waiting Times')
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
for num_servers in server_counts:
    waiting_times_traditional = simulate_queue(arrival_rate, service_rate_traditional, num_servers, int(num_requests_range[-1]))
    waiting_times_ndn = simulate_queue(arrival_rate, service_rate_ndn, num_servers, int(num_requests_range[-1]))
    
    # Calculate appropriate bin edges for a smoother CDF curve
    bins_traditional = np.linspace(0, max(waiting_times_traditional), 50)
    bins_ndn = np.linspace(0, max(waiting_times_ndn), 50)
    
    # Plot the CDF for the traditional service rate
    plt.hist(waiting_times_traditional, bins=bins_traditional, alpha=0.5, label=f'Traditional {num_servers} servers', density=True, cumulative=True, histtype='step')
    
    # Plot the CDF for the NDN service rate
    plt.hist(waiting_times_ndn, bins=bins_ndn, alpha=0.5, label=f'NDN {num_servers} servers', linestyle='--', density=True, cumulative=True, histtype='step')
    
    # Set the x-axis limit to focus on the more interesting part of the curve
    plt.xlim(0, np.percentile(waiting_times_ndn, 95))  # Show up to the 95th percentile of waiting times

plt.xlabel('Waiting Time (seconds)')
plt.ylabel('CDF')
plt.title('CDF of Waiting Times')
plt.legend(loc='lower right')  # Adjust the legend location if it's covering important parts of the plot
plt.grid(True)
plt.show()


