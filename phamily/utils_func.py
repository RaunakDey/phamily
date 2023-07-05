import logging
import sys
from scipy.integrate import odeint
import numpy as np
from nodes import Node, Connect


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
                dydt[node.id-1] += connect.connection_value
                logging.debug(f" The node ids are {node.id - 1}")
                # I am deleting this line, so 
                #dydt[connect.target.id-1] += connect.connection_value ## this bit is wrong???
        return dydt
    solution = odeint(system, initial_values, t)
    # Print the solution
    #for i, node in enumerate(Node.instances):
    #    print(f"{node.name} values at t=0: {initial_values[i]}")
    #    for j, time in enumerate(t):
    #        print(f"{node.name} values at t={time}: {solution[j][i]}")
    return solution




def connect_multi_compartment(list_of_nodes,name,parameters_input_list = None):
    '''
    Call the first node id
    '''
    if list_of_nodes[0].multiple_compartments == False:
        raise TypeError('wrong type of compartment, can not connect when there is only one compartment present.')
    
    id_start = list_of_nodes[0].id
    default_parameters = {
            'rate_of_tranfer' : 10,
        }
    if parameters_input_list is None:
        parameters_input_list = {}
    new_parameters = {key: parameters_input_list.get(key, default_parameters[key]) for key in default_parameters}

    for i in range(len(list_of_nodes)-1):
        connect_two_nodes = Connect(list_of_nodes[i],list_of_nodes[i+1],parameters_mega_list=new_parameters)
        value_of_the_function = connect_two_nodes.transfers(name='linear-transfer-forward')
        setattr(connect_two_nodes,'connection_value',value_of_the_function)
        
        
        connect_two_nodes_back = Connect(list_of_nodes[-1-i],list_of_nodes[-2-i])
        value_of_the_function_back = connect_two_nodes.transfers(name='linear-transfer-backward')
        setattr(connect_two_nodes_back,'connection_value',value_of_the_function_back)
        
 
        
    

    
    
    
        
        
