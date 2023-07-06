import logging
import sys
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


### This needs to be corrected.
sys.path.append('./../phamily/')

#More imports
from utils_func import solve_network, connect_multi_compartment
from nodes import Node, Connect


#from phamily import Node, Connect

# Set up logging configuration  
logging.basicConfig(level=logging.WARNING)

    
    
#agar = Node('nutrients', 'agar', value=12e5)
ecoli = Node('susceptible', 'ecoli', value=1e8)
lambda_virus = Node('free_virus','lambda',value= 1e7)
#exposed = Node('exposed','exposed-coli',multiple_compartments=True,latent=False,value = 0,number_of_latent_variables=5)

#connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)

# Print updated node values
for node in Node.instances:
    print(f"Before running stuff {node.name} value: {node.value}")
    


    
#Connect.create_connections()

#connection1 = Connect(agar,ecoli)
#connection1.connection_value = connection1.connections(name='type-I')

connection2 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'growth_rate':0.2, 'linear_model_mult_constant': 0.2}})
connection2.connection_value = connection2.connections(name = 'type-I' )

#connection3 = Connect(ecoli,lambda_virus,parameters_mega_list={(ecoli.type,lambda_virus.type):{'adsorption_rate':1.4e-13}})
#connection3.connection_value = connection3.connections(name='infect-and-lysis' )

#connection4 = Connect(lambda_virus,ecoli)
#connection4.connection_value = connection4.connections(name='infect-and-lysis')

#connection5 = Connect(ecoli,exposed,lambda_virus)
#connection5.connection_value = connection5.connections(name='new-infection')



# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 10.1, 0.1)
dt = time[1] - time[0]


### test a few stuff
'''
dydt = np.zeros(len(initial_values))
for node in Node.instances:
    for connect in node.connections.get(id(node), []):            
        dydt[node.id-1] += connect.connection_value
        print('dydt vector is {}'.format(dydt))
    node.value +=  dydt[node.id-1] * dt
    print(node.value)
    

for node in Node.instances:
    for connect in node.connections.get(id(node), []):            
        dydt[node.id-1] += connect.connection_value
        print('dydt vector second time is {}'.format(dydt))
'''





#Solving
solution = solve_network(time,initial_values)


for node in Node.instances:
    for connect in node.connections.get(id(node), []):
        #print(node.id -1)
        print(f"the source id is {connect.source.id} and the target id is {connect.target.id} and the value of the function is {connect.connection_value}" )       

#plotting


plt.plot(time, solution[:, 0], 'g', label='ecoli(t)')
plt.plot(time, solution[:, 1], 'b', label='lambda(t)')
plt.plot(time, solution[:, 2], 'r', label='first exposed compartment (t)')
plt.yscale('linear')
plt.show()



if __name__ == "__main__":
    print('Done. (C) Raunak Dey, Weitz Group.')
    print(f'The value of ecoli node is {ecoli.value}')

