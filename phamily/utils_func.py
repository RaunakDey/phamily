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
    solution = np.zeros([len(initial_values),len(t)])

    for node in Node.instances:
        node.time_series.append(initial_values[node.id-1])
        solution[node.id-1,0] = initial_values[node.id-1]
    
    for count in range(len(t)-1):
        for node in Node.instances:
            dydt = np.zeros(len(initial_values))
            for connect in node.connections.get(id(node), []): 
                ## I need to update these connections somehow???
                connect.update_connection_value()
                logging.error(f'Between {connect.source.name} and {connect.target.name} the value is {connect.connection_value}')
                dydt[node.id-1] += connect.connection_value if isinstance(connect.connection_value,(float,int)) is True else connect.connection_value[0]
                logging.debug(f" The node ids are {node.id - 1}")
                logging.debug(f'the dy is {dydt[node.id-1]*dt} between source {connect.source.name} with id {connect.source.id} and target {connect.target.name}, id {connect.target.id}')
            node.value +=  dydt[node.id-1] * dt
            solution[node.id-1,count+1] = node.value
            logging.debug(f'The node {node.name} has value {node.value}')
            #node.time_series.append(node.value)
            logging.debug(f'The time series of {node.name} is {node.time_series}')

    return solution
   


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
            setattr(connect_two_nodes,'name_of_func','linear-transfer-forward')
            
        for i in range(1,len(list_of_nodes)):    
            connect_two_nodes_back = Connect(list_of_nodes[i],list_of_nodes[i-1])
            value_of_the_function_back = connect_two_nodes.transfers(name='linear-transfer-backward')
            setattr(connect_two_nodes_back,'connection_value',value_of_the_function_back)
            setattr(connect_two_nodes_back,'name_of_func','linear-transfer-backward')
    elif type_of_transfer == 'exponential-decrease':
        raise NotImplemented
    elif type_of_transfer == 'exponential-increase':
        raise NotImplemented
    else:
        raise NotImplemented
        
 
        
    

    
    
    
        
        
