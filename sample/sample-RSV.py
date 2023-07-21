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

    

ecoli = Node('susceptible', 'ecoli', value=1e4)
lambda_virus = Node('free_virus','lambda',value= 2e3)
agar = Node('nutrients', 'agar', value=12e1)

    

    
#Connect.create_connections()

connection0 = Connect(agar,ecoli)
connection0.connection_value = connection0.connections(name='type-I')

connection1 = Connect(ecoli,agar)
connection1.connection_value = connection1.connections(name='type-I')


connection3 = Connect(ecoli,lambda_virus,parameters_mega_list={(ecoli.type,lambda_virus.type):{'adsorption_rate':1.4e-13}})
connection3.connection_value = connection3.connections(name='infect-and-lysis' )

connection4 = Connect(lambda_virus,ecoli)
connection4.connection_value = connection4.connections(name='infect-and-lysis')




# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 0.2, 0.01)
dt = time[1] - time[0]



solution = solve_network(time,initial_values)



plt.plot(time,solution[:,0],'g')
plt.plot(time,solution[:,1],'b')
plt.plot(time,solution[:,2],'r')
plt.yscale('log')
plt.show()


if __name__ == "__main__":
    print('Done. (C) Raunak Dey, Weitz Group.')


