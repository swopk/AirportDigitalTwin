This project is a simulation of an airport security checkpoint designed to study how disruptions affect passenger wait times. While labeled as a digital twin, it is essentially a discrete event simulation that models the flow of travelers through screening lanes. The goal is to quantify the resilience of the system when capacity is suddenly reduced, such as during a lane closure or staff shortage.

The simulation engine is built using the SimPy library and follows an M/M/c queuing model. This assumes that passenger arrivals follow a Poisson process and service times are exponentially distributed across multiple parallel lanes.

**Project Structure**
The repository consists of two primary Python modules:

- main.py: Contains the core simulation logic. It manages the passenger arrival generator, the stochastic service times, and a disruption manager that temporarily restricts lane availability. It uses a priority resource system to ensure that lane closures are handled realistically without losing passengers currently in the queue.

- dashboard.py: Handles data processing and visualization. It takes the raw event logs from the simulation and calculates performance metrics focusing on the cumulative extra wait time caused by disruptions.

**Technical Methodology**

The simulation calculates resilience by comparing the system state during a disruption against a calculated baseline.

- Arrivals: Defined by a lambda parameter representing passengers per minute.

- Service: Defined by a mu parameter representing the average processing capacity per lane.

- Resilience Metric: The primary output is the total person-minutes of delay, which is the area under the curve where wait times exceed normal operating conditions.

**Usage**

- Ensure all dependencies (see Requirements) are installed using pip.

- Run the simulation and generate the data log by executing main.py.

- Use dashboard.py to process the resulting CSV file and generate the performance graphs.

For now, sensitivity analysis can be done by adjusting the arrival and service variables in Main.py to identify the tipping point where the queue becomes unrecoverable.