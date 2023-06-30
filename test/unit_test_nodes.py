import logging
import sys
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
### This needs to be corrected.
sys.path.append('./../phamily/')

#More imports
from utils_func import solve_network
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



#Solving
solution = solve_network(time,initial_values)

#plotting

plt.plot(time, solution[:, 0], 'b', label='agar(t)')
plt.plot(time, solution[:, 1], 'g', label='ecoli(t)')
plt.plot(time, solution[:, 2], 'g', label='lambda(t)')
plt.show()

if __name__ == "__main__":
    print('DOne')