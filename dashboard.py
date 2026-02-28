import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load and Clean Data
df = pd.read_csv('airport_stats.csv')

# Define time intervals
T_START = 40
T_END = 80

# 2. Calculate Resilience Metrics
# Split data into phases
baseline = df[df['arrival'] < T_START]
disruption = df[(df['arrival'] >= T_START) & (df['arrival'] < T_END)]
recovery = df[df['arrival'] >= T_END]

# Compute Averages
avg_base = baseline['wait'].mean()
avg_disrupt = disruption['wait'].mean()
avg_recovery = recovery['wait'].mean()

# Quantify Resilience: "Person-Minutes of Delay"
# We compare actual wait times to the baseline average
df['extra_wait'] = (df['wait'] - avg_base).clip(lower=0)
resilience_loss = df[df['arrival'] >= T_START]['extra_wait'].sum()

# 3. Create Dashboard Visuals
plt.figure(figsize=(12, 10))

# Plot A: Wait Time Distribution
plt.subplot(2, 1, 1)
plt.scatter(df['arrival'], df['wait'], alpha=0.4, color='blue', label='Passenger Wait')
plt.plot(df['arrival'], df['wait'].rolling(10).mean(), color='black', label='Moving Avg (10 pax)')
plt.axvspan(T_START, T_END, color='red', alpha=0.1, label='Disruption (1 Lane)')
plt.title('Wait Time Spike Analysis')
plt.ylabel('Wait Time (Minutes)')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot B: Cumulative Resilience Loss
plt.subplot(2, 1, 2)
plt.fill_between(df['arrival'], df['extra_wait'].cumsum(), color='orange', alpha=0.3)
plt.plot(df['arrival'], df['extra_wait'].cumsum(), color='darkorange', label='Total System Delay')
plt.axvspan(T_START, T_END, color='red', alpha=0.1)
plt.title('Quantifying Resilience: Cumulative Delay (Person-Minutes)')
plt.xlabel('Arrival Time (Minutes)')
plt.ylabel('Cumulative Extra Wait')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('twin_dashboard.png')
plt.show()

#  4. Print Summary Report
print(f"DIGITAL TWIN PERFORMANCE REPORT")
print(f"Baseline Avg Wait: {avg_base:.2f} min")
print(f"Disruption Avg Wait: {avg_disrupt:.2f} min")
print(f"Recovery Avg Wait: {avg_recovery:.2f} min")
print(f"RESILIENCE LOSS: {resilience_loss:.2f} person-minutes")