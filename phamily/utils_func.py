import logging
import sys
from scipy.integrate import odeint, solve_ivp
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
                #logging.error(f'Between {connect.source.name} and {connect.target.name} the value of function {connect.name_of_func} is {connect.connection_value}, where source value is {connect.source.value} and target value is {connect.target.value}')
                dydt[node.id-1] += connect.connection_value if isinstance(connect.connection_value,(float,int)) is True else connect.connection_value[0]
                logging.debug(f" The node ids are {node.id - 1}")
                logging.debug(f'the dy is {dydt[node.id-1]*dt} between source {connect.source.name} with id {connect.source.id} and target {connect.target.name}, id {connect.target.id}')
            node.value +=  dydt[node.id-1] * dt
            solution[node.id-1,count+1] = node.value
            #logging.error(f'The node {node.name} has value {node.value}')
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
            setattr(node,'value',y[node.id-1])
            for connect in node.connections.get(id(node), []):
                connect.update_connection_value()
                dydt[node.id-1] += connect.connection_value if isinstance(connect.connection_value,(float,int)) is True else connect.connection_value[0]
                logging.debug(f" The node ids are {node.id - 1}")
                # I am deleting this line, so 
                #dydt[connect.target.id-1] += connect.connection_value ## this bit is wrong???
            # this way I keep on updating the node values.
            
            #logging.error(f'value of node {node.name} is {node.value}')
        return dydt
    

    solution = odeint(system,initial_values,t,mu=0,ml=0,rtol=1e-10,atol=1e-10)
    #solution = solve_ivp(system,t_span=(t[0],t[-1]),y0=initial_values)
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
            setattr(connect_two_nodes,'parameters_mega_list',new_parameters)
            #logging.error(
            #    f'The attributed parameters of transfer between {connect_two_nodes.source.name} and {connect_two_nodes.target.name} are {connect_two_nodes.parameters_mega_list}'
            #              )
        for i in range(1,len(list_of_nodes)):    
            connect_two_nodes_back = Connect(list_of_nodes[i],list_of_nodes[i-1])
            value_of_the_function_back = connect_two_nodes.transfers(name='linear-transfer-backward')
            setattr(connect_two_nodes_back,'connection_value',value_of_the_function_back)
            setattr(connect_two_nodes_back,'name_of_func','linear-transfer-backward')
            setattr(connect_two_nodes_back,'parameters_mega_list',new_parameters)
            #logging.error(
            #    f'The attributed parameters of transfer between {connect_two_nodes_back.source.name} and {connect_two_nodes_back.target.name} are {connect_two_nodes_back.parameters_mega_list}'
            #              )
    elif type_of_transfer == 'exponential-decrease':
        raise NotImplemented
    elif type_of_transfer == 'exponential-increase':
        raise NotImplemented
    else:
        raise NotImplemented



## TO DO
def connect_lastcompartment_to_one(the_first_node,Node,the_target_node,func_name,parameters_input_list = None):
    ### Both way
    if not the_first_node.multiple_compartments:
        raise TypeError('wrong type of compartment, can not connect when there is only one compartment present.')
    

    default_parameters = {
                'rate_of_tranfer': 1e1,
                'burst_size' : 200
            }
    if parameters_input_list is None:
        parameters_input_list = {}
    new_parameters = {key: parameters_input_list.get(key, default_parameters[key]) for key in default_parameters}
    

    number_of_nodes = the_first_node.number_of_latent_variables
    the_last_node = next(filter(lambda node: node.id == (the_first_node.id + the_first_node.number_of_latent_variables -1), Node.instances), None)
    connection_last2target = Connect(the_last_node,the_target_node, parameters_mega_list=new_parameters )
    value = connection_last2target.connections(name=func_name)
    setattr(connection_last2target,'connection_value',value)
    setattr(connection_last2target,'name_of_func',func_name)
    setattr(connection_last2target,'parameters_mega_list',new_parameters)

    connection_target2last = Connect(the_target_node,the_last_node,parameters_mega_list=new_parameters)
    value = connection_target2last.connections(name=func_name)
    setattr(connection_target2last,'connection_value',value)
    setattr(connection_target2last,'name_of_func',func_name)
    setattr(connection_target2last,'parameters_mega_list',new_parameters)
    


def connect_2_multicompartments(first_node_one,first_node_two,type_of_transfer,parameters_input_list = None):
    if first_node_one.multiple_compartments is False or first_node_two.multiple_compartments is False:
        raise TypeError('can not connect single compartments, use connections method instead.')
    if not first_node_one.number_of_latent_variables == first_node_two.number_of_latent_variables:
        raise TypeError('unqual number of compartments. Cannot be connected.')
    
    #actual method
    default_parameters = {
            'linear-transfer-rate' : 10,
        }
    if parameters_input_list is None:
        parameters_input_list = {}
    new_parameters = {key: parameters_input_list.get(key, default_parameters[key]) for key in default_parameters}
    node_one_list =[]
    node_two_list = []
    node_one_list.append(first_node_one)
    node_two_list.append(first_node_two)

    for node in Node.instances:
        if node.id > first_node_one.id and node.id < first_node_one.id + first_node_one.number_of_latent_variables:
            node_one_list.append(node)
        elif node.id > first_node_two.id and node.id < first_node_two.id + first_node_two.number_of_latent_variables:
            node_two_list.append(node)
    if type_of_transfer == 'linear':
        for i in range(0,first_node_one.number_of_latent_variables-1):
            connect_fwd = Connect(node_one_list[i],node_two_list[i],parameters_mega_list=new_parameters)
            value_of_the_function = connect_fwd.transfers(name='linear-transfer-forward')
            setattr(connect_fwd,'connection_value',value_of_the_function)
            setattr(connect_fwd,'name_of_func','linear-transfer-forward')
            setattr(connect_fwd,'parameters_mega_list',new_parameters)

            connect_bkw = Connect(node_two_list[i],node_one_list[i],parameters_mega_list=new_parameters)
            value_of_the_function - connect_bkw.transfers(name='linear-transfer-backward')
            setattr(connect_bkw,'connection_value',value_of_the_function)
            setattr(connect_bkw,'name_of_func','linear-transfer-forward')
            setattr(connect_bkw,'parameters_mega_list',new_parameters)
    if type_of_transfer == 'exponential':
        raise NameError('to be implemented later. Sorry')

    # incomplete.

def connect_one_to_multi(starting_node,first_of_multi_node,Node,parameters_input_list,func_name):
    number_of_nodes = first_of_multi_node.number_of_latent_variables
    list_of_nodes = []
    list_of_nodes.append(first_of_multi_node)
    for node in Node.instances:
        if node.id > first_of_multi_node.id and node.id < first_of_multi_node.id + first_of_multi_node.number_of_latent_variables:
            list_of_nodes.append(node)
        logging.warning(f'The nodes are list {node.name}')

    default_parameters = {
                'rate_of_tranfer': 1e1,
                'burst_size' : 200
            }
    if parameters_input_list is None:
        parameters_input_list = {}
    new_parameters = {key: parameters_input_list.get(key, default_parameters[key]) for key in default_parameters}
    

    for i in range(0,number_of_nodes):
        connecting_one_multi = Connect(starting_node,list_of_nodes[i],parameters_mega_list=new_parameters)
        value = connecting_one_multi.connections(name=func_name)
        setattr(connecting_one_multi,'connection_value',value)
        setattr(connecting_one_multi,'name_of_func',func_name)
        setattr(connecting_one_multi,'parameters_mega_list',new_parameters)


def connect_multi_to_one():
    raise NotImplemented

#### properties of dynamical system:
def find_equilibirum_points(Node,Connect):
    '''
    Finds fixed points given the nodes and connections, with stabibility analysis.
    '''
    raise NotImplemented

def bifurcation_finder(Node,Connect):
    '''
    Finds hyper-parameter where you can change in stability properties.
    '''
    raise NotImplemented

def stable_parameters_finder(Node,Connect):
    '''
    Find zones of stable parameter sets, where the population does not crash--
    Either becomes stationary, or becomes periodic.
    '''
    raise NotImplemented
    

    
    
    
        
        
