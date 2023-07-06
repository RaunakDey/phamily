import logging
import sys
from scipy.integrate import odeint
import numpy as np
from nodes import Node, Connect

def solve_network_euler(
    t: any,
    initial_values: any
    ) -> None:
    '''
    time: solution timescales
    initial_values: initial values of all the nodes in the phamily network.
    '''
    dt = t[1]-t[0]
    for count in range(len(t)):
        dydt = np.zeros(len(initial_values))
        for node in Node.instances:
            for connect in node.connections.get(id(node), []): 
                ## I need to update these connections somehow???
                dydt[node.id-1] += connect.connection_value
                logging.debug(f" The node ids are {node.id - 1}")
            node.value +=  dydt * dt
        
    
   
        
   


# has terrible bugs -- to be fixed
def solve_network(
    t: any,
    initial_values: any
    ) -> None:
    '''
    has terrible bugs -- to be fixed -- do not use now
    time: solution timescales
    initial_values: initial values of all the nodes in the phamily network.
    '''
    # Define the system of differential equationsx
    
    dt = t[1]-t[0]
    
    def system(y, t):
        dydt = np.zeros(len(y))
        for node in Node.instances:
            for connect in node.connections.get(id(node), []):
                dydt[node.id-1] += connect.connection_value
                logging.debug(f" The node ids are {node.id - 1}")
                # I am deleting this line, so 
                #dydt[connect.target.id-1] += connect.connection_value ## this bit is wrong???
            node.value +=  dydt[node.id-1] * dt
        return dydt
    solution = odeint(system, initial_values, t)
    return solution




def connect_multi_compartment(the_first_node,Node,type_of_transfer,parameters_input_list = None):
    '''
    Call the first node id
    '''
    if the_first_node.multiple_compartments == False:
        raise TypeError('wrong type of compartment, can not connect when there is only one compartment present.')
    
    
    number_of_nodes = the_first_node.number_of_latent_variables
    id_start = the_first_node.id
    default_parameters = {
            'linear-transfer-rate' : 10,
        }
    if parameters_input_list is None:
        parameters_input_list = {}
    new_parameters = {key: parameters_input_list.get(key, default_parameters[key]) for key in default_parameters}
    
    list_of_nodes = []
    list_of_nodes.append(the_first_node)
    for node in Node.instances:
        if node.id > the_first_node.id and node.id < the_first_node.id + the_first_node.number_of_latent_variables:
            list_of_nodes.append(node)
        logging.warning(f'The nodes are list {node.name}')
    
    if type_of_transfer == 'linear':
        for i in range(0,number_of_nodes-1):
            connect_two_nodes = Connect(list_of_nodes[i],list_of_nodes[i+1],parameters_mega_list=new_parameters)
            value_of_the_function = connect_two_nodes.transfers(name='linear-transfer-forward')
            setattr(connect_two_nodes,'connection_value',value_of_the_function)
            
        for i in range(1,len(list_of_nodes)):    
            connect_two_nodes_back = Connect(list_of_nodes[i],list_of_nodes[i-1])
            value_of_the_function_back = connect_two_nodes.transfers(name='linear-transfer-backward')
            setattr(connect_two_nodes_back,'connection_value',value_of_the_function_back)
    elif type_of_transfer == 'exponential-decrease':
        raise NotImplemented
    elif type_of_transfer == 'exponential-increase':
        raise NotImplemented
    else:
        raise NotImplemented
        
 
        
    

    
    
    
        
        
