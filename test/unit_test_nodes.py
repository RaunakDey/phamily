import logging
import sys
from scipy.integrate import odeint
import numpy as np

sys.path.append('./../phamily/')

from nodes import Node, Connect
#from phamily import Node, Connect

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

    
    
agar = Node('nutrients', 'agar', value=12e5)
ecoli = Node('susceptible', 'ecoli', value=1e4)
lambda_virus = Node('free_virus','lambda',value= 1e8)

# Print updated node values
for node in Node.instances:
    print(f"Before running stuff {node.name} value: {node.value}")

connection1 = Connect(agar,ecoli)
connection1.connection_value = connection1.connections(name='type-I')

connection2 = Connect(ecoli)
connection2.connection_value = connection2.connections(name = 'self-growth' )

connection3 = Connect(ecoli,lambda_virus)
connection3.connection_value = connection3.connections(name='infect-and-lysis' )

connection4 = Connect(lambda_virus,ecoli)
connection4.connection_value = connection4.connections(name='infect-and-lysis')


# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)


# Update node values using connection values
for node in Node.instances:
    for connect in node.connections.get(id(node), []):
        node.value -= connect.connection_value

# Print updated node values
for node in Node.instances:
    print(f"{node.name} value: {node.value}")

## integration step
'''
def differential_equation(t,y):
    #t is a scalar and y is an ndarray with len(y) = y0 and function  returns  an array of the same shape as y
    dydt = y*t
    return dydt


# Set up initial conditions
initial_conditions = [agar.value, ecoli.value, lambda_virus.value]

# Set up the time span for integration
start_time = 0
end_time = 10
num_time_points = 1000
t = np.linspace(start_time, end_time, num_time_points)

# Solve the differential equations
solution = odeint(differential_equation, initial_conditions, t)
print(solution)
'''