import logging
import sys
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('./../phamily/')
#from ..phamily.utils_func import solve_network 

from nodes import Node, Connect
#from phamily import Node, Connect

# Set up logging configuration  
logging.basicConfig(level=logging.WARNING)

    
    
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

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 10.1, 0.1)



### function  -- to be moved

def solve_network(
    t: any,
    initial_values: any
    ) -> None:
    '''
    time: solution timescales
    initial_values: initial values of all the nodes in the phamily network.
    '''
    # Define the system of differential equations
    def system(y, t):
        dydt = np.zeros(len(y))
        for node in Node.instances:
            for connect in node.connections.get(id(node), []):
                dydt[node.id-1] -= connect.connection_value
                dydt[connect.target.id-1] += connect.connection_value
        return dydt
    solution = odeint(system, initial_values, t)
    # Print the solution
    #for i, node in enumerate(Node.instances):
    #    print(f"{node.name} values at t=0: {initial_values[i]}")
    #    for j, time in enumerate(t):
    #        print(f"{node.name} values at t={time}: {solution[j][i]}")
    return solution




#Solving
solution = solve_network(time,initial_values)

#plotting

plt.plot(time, solution[:, 0], 'b', label='agar(t)')
plt.plot(time, solution[:, 1], 'g', label='ecoli(t)')
plt.plot(time, solution[:, 2], 'g', label='lambda(t)')
plt.show()
'''
# Update node values using connection values
for node in Node.instances:
    for connect in node.connections.get(id(node), []):
        node.value -= connect.connection_value

# Print updated node values
for node in Node.instances:
    print(f"{node.name} value: {node.value}")
'''
