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

    
    
#agar = Node('nutrients', 'agar', value=12e5)
ecoli = Node('susceptible', 'ecoli', value=1e8)
lambda_virus = Node('free_virus','lambda',value= 2e7)
#exposed = Node('exposed','exposed-coli',multiple_compartments=True,latent=True,value = 0,number_of_latent_variables=3)
#connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)




    
#Connect.create_connections()


connection2 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'growth_rate':5, 'linear_model_mult_constant': 5}})
connection2.connection_value = connection2.connections(name = 'type-I' )

connection3 = Connect(ecoli,lambda_virus,parameters_mega_list={(ecoli.type,lambda_virus.type):{'adsorption_rate':1.4e-8}})
connection3.connection_value = connection3.connections(name='infect-and-lysis' )

connection4 = Connect(lambda_virus,ecoli,parameters_mega_list={(ecoli.type,lambda_virus.type):{'adsorption_rate':1.4e-8}})
connection4.connection_value = connection4.connections(name='infect-and-lysis')

#connection5 = Connect(ecoli,exposed,lambda_virus)
#connection5.connection_value = connection5.connections(name='new-infection')

#connection6 = Connect(exposed,ecoli,lambda_virus)
#connection6.connection_value = connection6.connections(name='new-infection')

#connect_lastcompartment_to_one(exposed,Node,lambda_virus,func_name='lysis')


# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]


# Time points
time = np.arange(0, 0.5, 0.01)
dt = time[1] - time[0]



solution = solve_network_euler(time,initial_values)

#print(solution[:,0])
#print(f'Ecoli time series is {ecoli.time_series}')
#print(f'Lambda time series is {lambda_virus.time_series}')
#plt.plot(time,solution[:,0],'g')
#plt.plot(time,solution[:,1],'b')

plt.plot(time,solution[0,:],'g')
plt.plot(time,solution[1,:],'b')

#plt.plot(time,solution[:,2],'r')
plt.yscale('log')
plt.show()





  




if __name__ == "__main__":
    print('Done. (C) Raunak Dey, Weitz Group.')


