import simpy 
import random
import pandas as pd
import matplotlib.pyplot as plt

RANDOM_SEED = 42
SIM_TIME = 120
LAMBDA = 2.0
MU = 0.8
NUM_LANES = 4
performance_log = []
queue_history = []
def passenger(env, name, checkpoint_container):
    arrival_time = env.now
    #print(name + " arrived at " + str(round(arrival_time, 2)))

    with checkpoint_container['resource'].request(priority=0) as request:
        yield request
        
        wait_time = env.now - arrival_time
        #print(name + " started screening at " + str(round(env.now, 2)) + " (Wait: " + str(round(wait_time, 2)) + ")")
        # Log the data into our list
        performance_log.append({
            'name': name,
            'arrival': arrival_time,
            'wait': wait_time,
            'service_start': env.now
        })
        service_duration = random.expovariate(MU)
        yield env.timeout(service_duration)
        
        #print(name + " finished at " + str(round(env.now, 2)))
def queue_monitor(env, checkpoint_container):
    while True:
    # Look at how many people are currently in the 'queue'
        current_wait_count = len(checkpoint_container['resource'].queue)
    # Record the time and the count
        queue_history.append({
        'time': env.now,
        'queue_length': current_wait_count
        })
        # Wait 1 minute before checking again
        yield env.timeout(1)

def arrival_generator(env, checkpoint_container):
    p_id = 0
    while True:
        inter_arrival = random.expovariate(LAMBDA)
        yield env.timeout(inter_arrival)
        
        p_id = p_id + 1
        env.process(passenger(env, "Pax_" + str(p_id), checkpoint_container))

def disruption_manager(env, checkpoint_container):
    yield env.timeout(40)
    print("--- DISRUPTION START: 3 LANES CLOSED ---")
    #checkpoint_container['resource'] = simpy.Resource(env, capacity=1)
    # Store the 'claims' on the lanes so we can release them later
    staff_claims = []
    for i in range(3):
        # priority=-1 makes the staff 'jump' to the front of the line
        req = checkpoint_container['resource'].request(priority=-1)
        staff_claims.append(req)
        yield req  # The staff now 'occupies' the lane
        yield env.timeout(40)
    print("--- DISRUPTION END: LANES REOPENED ---")
    #checkpoint_container['resource'] = simpy.Resource(env, capacity=4)
    for req in staff_claims:
        checkpoint_container['resource'].release(req)

print("--- STARTING SECURITY CHECKPOINT SIMULATION ---")
random.seed(RANDOM_SEED)
env = simpy.Environment()
checkpoint_container = {'resource': simpy.PriorityResource(env, capacity=NUM_LANES)}
env.process(arrival_generator(env, checkpoint_container))
env.process(disruption_manager(env, checkpoint_container))
# New: Start the camera
env.process(queue_monitor(env, checkpoint_container))
env.run(until=SIM_TIME)


# Convert our list of dictionaries into a clean Table (DataFrame)
df = pd.DataFrame(performance_log)

# Calculate the Average Wait Time
avg_wait = df['wait'].mean()
max_wait = df['wait'].max()

#print("SIMULATION COMPLETE")
#print("Average Wait Time: " + str(round(avg_wait, 2)) + " minutes")
#print("Maximum Wait Time: " + str(round(max_wait, 2)) + " minutes")


# 1. Create a table for the Queue Length history
df_q = pd.DataFrame(queue_history)
df_p = pd.DataFrame(performance_log)
# 2. Start the Plot
plt.figure(figsize=(10, 6))
plt.plot(df_q['time'], df_q['queue_length'], color='blue', label='Queue Length')

# 3. Mark the Disruption Area in Red
plt.axvspan(40, 80, color='red', alpha=0.2, label='Disruption (1 Lane)')

# 4. Add Labels and Title
plt.title('Airport Digital Twin: Security Checkpoint Resilience')
plt.xlabel('Time (Minutes)')
plt.ylabel('Passengers in Line')
plt.legend()
plt.grid(True)

# Calculate the 'Baseline' wait (Average wait before minute 40)
baseline_wait = df[df['arrival'] < 40]['wait'].mean()

# Calculate the 'Disruption Impact'
# We sum the wait times that occurred after the disruption started
total_extra_wait = df[df['arrival'] >= 40]['wait'].sum()

print("--- RESILIENCE METRICS ---")
print("Total Extra Wait Time (Person-Minutes): " + str(round(total_extra_wait, 2)))
# 5. Show the Graph
plt.show()
df.to_csv('airport_stats.csv', index=False)