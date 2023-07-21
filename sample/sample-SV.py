import logging
import sys
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


### This needs to be corrected.
sys.path.append('./../phamily/')

#More imports
from utils_func import *
from nodes import Node, Connect


#from phamily import Node, Connect

# Set up logging configuration  
logging.basicConfig(level=logging.ERROR)

    
    
latent_period = 1

ecoli = Node('susceptible', 'ecoli', value=1e4)
lambda_virus = Node('free_virus','lambda',value= 2e3)



    
#Connect.create_connections()

#E-coli growing

connection1 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'growth_rate':1, 'linear_model_mult_constant': 1}})
connection1.connection_value = connection1.connections(name = 'type-I' )

connection2 = Connect(ecoli,lambda_virus,parameters_mega_list={(ecoli.type,lambda_virus.type):{'adsorption_rate':1.4e-13}})
connection2.connection_value = connection2.connections(name='infect-and-lysis' )

connection3 = Connect(lambda_virus,ecoli)
connection3.connection_value = connection3.connections(name='infect-and-lysis')

# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 20, 0.01)
dt = time[1] - time[0]



solution = solve_network_euler(time,initial_values)

#print(solution)
fig, ax = plt.subplots()
ax.plot(time,solution[0,:],'g',label = 'susceptible hosts')
ax.plot(time,solution[1,:],'b',label = 'phage')
ax.legend(loc='upper left', frameon=False)
plt.yscale('log')
plt.xlabel('Time (hour)')
plt.ylabel('population')

plt.show()
fig



for node in Node.instances:
    print(node.name)

  




if __name__ == "__main__":
    print('Done. (C) Raunak Dey, Weitz Group.')


