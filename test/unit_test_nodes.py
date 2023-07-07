import logging
import sys
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


### This needs to be corrected.
sys.path.append('./../phamily/')

#More imports
from utils_func import solve_network, connect_multi_compartment, solve_network_euler
from nodes import Node, Connect


#from phamily import Node, Connect

# Set up logging configuration  
logging.basicConfig(level=logging.ERROR)

    
    
#agar = Node('nutrients', 'agar', value=12e5)
ecoli = Node('susceptible', 'ecoli', value=1e8)
lambda_virus = Node('free_virus','lambda',value= 2e7)
#exposed = Node('exposed','exposed-coli',multiple_compartments=True,latent=False,value = 0,number_of_latent_variables=5)

#connect_multi_compartment(exposed,Node,type_of_transfer='linear',parameters_input_list = None)

# Print updated node values
for node in Node.instances:
    print(f"Before running stuff {node.name} value: {node.value}")
    

    
#Connect.create_connections()

#connection1 = Connect(agar,ecoli)
#connection1.connection_value = connection1.connections(name='type-I')

connection2 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'growth_rate':5, 'linear_model_mult_constant': 5}})
connection2.connection_value = connection2.connections(name = 'type-I' )

connection3 = Connect(ecoli,lambda_virus,parameters_mega_list={(ecoli.type,lambda_virus.type):{'adsorption_rate':1.4e-13}})
connection3.connection_value = connection3.connections(name='infect-and-lysis' )

connection4 = Connect(lambda_virus,ecoli)
connection4.connection_value = connection4.connections(name='infect-and-lysis')

#connection5 = Connect(ecoli,exposed,lambda_virus)
#connection5.connection_value = connection5.connections(name='new-infection')



# Collect the values of all Node instances
node_values = [node.value for node in Node.instances]
values_array = np.array(node_values)

# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 5, 0.01)
dt = time[1] - time[0]



solution = solve_network_euler(time,initial_values)
print(solution[0,:])
#print(f'Ecoli time series is {ecoli.time_series}')
#print(f'Lambda time series is {lambda_virus.time_series}')
plt.plot(time,solution[0,:],'g')
plt.plot(time,solution[1,:],'b')
plt.yscale('log')
plt.show()



'''
# testing some stuff on local
#print(f'the node value is before {node.value}')
dt = time[1]-time[0]
dydt = np.zeros(len(initial_values))
for node in Node.instances:
    for connect in node.connections.get(id(node), []):
        connect.update_connection_value()
        dydt[node.id-1] += connect.connection_value
        print(f'the connection_value before is {connect.connection_value}')
        #print(isinstance(connect.connection_value,float))
    node.value += dydt * dt
    #print(f'the node value after is {node.value}')
    #print(f'the dydt value before is {dydt}')
    for connect in node.connections.get(id(node), []):
        connect.update_connection_value()
        dydt[node.id-1] += connect.connection_value[0]
        print(f'the connection_value after is {connect.connection_value}')
        #print(isinstance(connect.connection_value,float))
    node.value += dydt * dt
    #print(f'the node value after is {node.value}')
    for connect in node.connections.get(id(node), []):
        connect.update_connection_value()
        dydt[node.id-1] += connect.connection_value[0]
        print(f'the connection_value after is {connect.connection_value}')
    node.value += dydt * dt
    #print(f'the node value after is {node.value}')


'''







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


'''


if __name__ == "__main__":
    print('Done. (C) Raunak Dey, Weitz Group.')
    print(f'The value of ecoli node is {ecoli.value}')


