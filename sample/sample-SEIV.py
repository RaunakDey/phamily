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
ecoli = Node('susceptible', 'ecoli', value=1e4)
lambda_virus = Node('free_virus','lambda',value= 2e3)
exposed = Node('exposed','exposed-coli',multiple_compartments=True,latent=True,value = 0,number_of_latent_variables=3)
connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)


    

    
#Connect.create_connections()

#E-coli growing
connection1 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'growth_rate':1, 'linear_model_mult_constant': 1}})
connection1.connection_value = connection1.connections(name = 'type-I' )

#Ecoli getting exposed
connection2 = Connect(ecoli,exposed,lambda_virus)
connection2.connection_value = connection2.connections(name='new-infection')

#Exposed cells grow
connection3 = Connect(exposed,ecoli,lambda_virus)
connection3.connection_value = connection3.connections(name='new-infection')

#Transition across exposed compartments
connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)
### Debug this!!!!
connect_lastcompartment_to_one(exposed,Node,lambda_virus,func_name='lysis')

# Virus getting adsorped to all types of hosts
connect_one_to_multi(lambda_virus,exposed,Node,parameters_input_list=None,func_name='adsorption')
connection4 = Connect(lambda_virus,ecoli)
connection4.connection_value = connection4.connections(name='adsorption')

# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 2, 0.01)
dt = time[1] - time[0]



solution = solve_network_euler(time,initial_values)



plt.plot(time,solution[0,:],'g')
plt.plot(time,solution[1,:],'b')
plt.plot(time,solution[4,:],'r')
plt.yscale('log')
plt.show()



for node in Node.instances:
    print(node.name)


  




if __name__ == "__main__":
    print('Done. (C) Raunak Dey, Weitz Group.')


