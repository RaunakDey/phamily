from dataclasses import dataclass
import logging
import numpy as np

@dataclass
class Node:
    type: str = None
    name: str = None
    metadata: str = None
    units: str = None
    value: float = None
    multiple_compartments: bool = False
    latent : bool = False
    number_of_latent_variables: int = 10
    id: int = None
    _id_counter: int = 0
    connections = {}
    time_series = [] 
    
    '''
    creates new ids for new nodes.
    '''
    # Separate list to keep track of all node instances
    instances = []

    def __post_init__(self):
        ### add list of nodes above this
        # Keeping track of node serial numbers
        if self.type not in ['susceptible', 'free_virus', 'nutrients','exposed','outside']:
            raise ValueError("Invalid Node type")
        
        Node._id_counter += 1
        self.id = Node._id_counter
        
        
        
        # Dealing with latent nodes
        if self.multiple_compartments:
            #latent_nodes = []
            for i in range(1, self.number_of_latent_variables):
                new_node = Node(
                    type=self.type,
                    name=f"{self.name}{self.id+i}",
                    metadata=self.metadata, 
                    units=self.units,
                    value=self.value,
                    multiple_compartments =  False,
                    latent = True
                )
                #latent_nodes.append(new_node)
            #self.__class__.instances.extend(latent_nodes)
            
        # keeping a collection of instances for these nodes.
        self.__class__.instances.append(self)
        
        
    def __str__(self):
        return f"Node(type={self.type}, name={self.name}, value = {self.value}, latent = {self.latent}, id = {self.id})"


@dataclass
class Connect:
    source: Node = None
    target: Node = None
    other_helper : Node = None
    parameters_mega_list: dict = None
    instances = []
    connection_value: float = None
    name_of_func: str = None
    
    '''
    if there is no target, it selects the source as the target 
    '''
    
    def __post_init__(self):
        self.target = self.source if self.target is None else self.target
        # keeping a collection of instances for these edges.
        self.__class__.instances.append(self)
        #self.source.connections.setdefault(self.source, []).append(self)
        self.source.connections.setdefault(id(self.source), []).append(self)
        if self.parameters_mega_list is None:
            self.parameters_mega_list = {}  # Set an empty dictionary as the default value
            
    

    def connections(self, name: str):
        name = self.name_of_func if self.name_of_func is not None else name
        source = self.source
        target = self.target if self.target is not None else self.source
        key = (source.type, target.type)
        #parameters = self.parameters_mega_list.get(key, {}) if self.parameters_mega_list is not None else {}
        parameters = self.parameters_mega_list.get(key, {})
        #### Can use mapping and lambda function to optimize this
        
        if source.type == 'nutrients' and target.type == 'susceptible':
            default_parameters = {
                'linear_model_mult_constant': 0.5,
                'half_conc': 1,
                'monod_mult_constant': 0.1
            }
            parameters = {**default_parameters, **parameters}

            if name == 'self-growth':
                value = 1
            elif name == 'type-I' or name is None:
                linear_model_mult_constant = parameters['linear_model_mult_constant']
                value = linear_model_mult_constant * self.source.value
            elif name == 'monod':
                half_conc = parameters['half_conc']
                monod_mult_constant = parameters['monod_mult_constant']
                value = monod_mult_constant * self.source.value / (half_conc + self.source.value)
            else:
                raise NameError('wrong name of function')
            
        
        elif source.type == 'nutrients' and target.type == 'outside':
            default_parameters = {'inflow_rate' : 1,'outflow_rate' : 1,'flux' : 1}
            parameters = {**default_parameters,**parameters}
            if name == 'media-inflow':
                inflow_rate = parameters['inflow_rate']
                flux = parameters['flux']
                value = inflow_rate*flux
            elif name == 'outflow':
                outflow_rate = parameters['outflow_rate']
                value = -outflow_rate*source.value
            else:
                raise NameError('wrong name of function')

        elif source.type == 'susceptible' and target.type == 'susceptible':
            default_parameters = {
                'growth_rate' : 1,
                'linear_model_mult_constant': 0.5,
                'half_conc': 1,
                'monod_mult_constant': 1,
                'carrying_cap' : 1e4,
                'outflow_rate' : 1
            }
            parameters = {**default_parameters, **parameters}
            logging.warning("The parameters used are {}".format(parameters))
            if name == 'self-growth' or name is None:
                growth_rate = parameters['growth_rate']
                value = growth_rate*source.value
            elif name == 'logistic-growth':
                carrying_cap = parameters['carring_cap']
                growth_rate = parameters['growth_rate']
                value = growth_rate*source.value*(1 - (source.value/carrying_cap))
            elif name == 'type-I':
                linear_model_mult_constant = parameters['linear_model_mult_constant']
                value = linear_model_mult_constant * self.source.value
            elif name == 'monod':
                half_conc = parameters['half_conc']
                monod_mult_constant = parameters['monod_mult_constant']
                value = monod_mult_constant * self.source.value / (half_conc + self.source.value)
            elif name == 'outflow':
                outflow_rate = parameters['outflow_rate']
                value = -outflow_rate*source.value
            else:
                raise NameError('wrong name of function')
        
        elif source.type == 'susceptible' and target.type == 'free_virus':
            default_parameters = {
                'adsorption_rate' : 1.4e-13,
            } 
            parameters = {**default_parameters, **parameters}
            logging.warning("The parameters used are {}".format(parameters))
            if name == 'infect-and-lysis' or name is None:
                adsorption_rate = parameters['adsorption_rate']
                value = -adsorption_rate*source.value*target.value
            else:
                raise NameError('wrong name of function')
            
        elif source.type == 'free_virus' and target.type == 'susceptible':
            default_parameters = {
                'adsorption_rate' : 1.4e-13,
                'burst_size' : 350
            } 
            parameters = {**default_parameters, **parameters}
            if name == 'infect-and-lysis' or name is None:
                adsorption_rate = parameters['adsorption_rate']
                burst_size = parameters['burst_size']
                value = burst_size*adsorption_rate*source.value*target.value
            else:
                raise NameError('wrong name of function')
            
        elif source.type == 'susceptible' and target.type == 'exposed' and self.other_helper.type == 'free_virus':
            default_parameters = {
                'number_of_compartments' : 10,
                'rate_of_tranfer': 0.1,
                'adsorption_rate' : 1e-10
            }
            parameters = {**default_parameters, **parameters}
            if name == 'new-infection' or name is None:
                number_of_compartments = parameters['number_of_compartments']
                rate_of_transfer = parameters['rate_of_tranfer']
                adsorption_rate = parameters['adsorption_rate']
                value = -adsorption_rate*source.value*self.other_helper.value
            else:
                raise NameError('wrong name of function')
            logging.warning(f'The value is {value}')
        
    
                
                
        ## Just add lines above this
        #logging.debug(
        #        "The value returned by the {} function between {} and {} for the parameters {} is {}".format(
        #            name, source.type, target.type, parameters, value
        #        )
        #    )
        return value
        self.connection_value = value
        self.name_of_func = name
    
    
    def transfers(self,name):
        parameters = self.parameters_mega_list
        linear_rate = parameters.get('linear-transfer-rate')
        if name == 'linear-transfer-forward' or name is None:    
            value = -linear_rate*self.source.value
        elif name == 'linear-transfer-backward':
            value = +linear_rate*self.target.value
        elif name == 'exponential-decay':
            pass
        else:
            raise NameError('Undefined function. Please check the name of the function used.')
        return value
        self.connection_value = value
        self.name_of_func = name
    
    def update_connection_value(self):
        source = self.source
        target = self.target
        other_helper = self.other_helper
        name_of_func_used = self.name_of_func
        if source.latent is False or target.latent is False:
            logging.error(f'source is {source.name}, target is {target.name}')
            self.connection_value = self.connections(name=name_of_func_used)
        # for the tranfer function I need to rewrite the last two lines, that if the nodes is multicompartments,
        # then I would use the transfer function and name of the function to update this.
        elif source.latent is True and target.latent is True:
            self.connection_value = self.transfers(name=name_of_func_used)
        else:
            raise TypeError


    # not tested.
    @classmethod
    def create_connections(cls):
        connected_nodes = set([connect.source for connect in cls.instances] +
                              [connect.target for connect in cls.instances if connect.target is not None])

        unconnected_nodes = set(Node.instances) - connected_nodes

        for i, source in enumerate(unconnected_nodes, start=1):
            target = source  # Make a self-connection by default
            connection_name = f"connection{i}"

            connect = Connect(source, target)
            setattr(connect, "name", connection_name)

            logging.debug(f"Created connection '{connection_name}' between {source} and {target}")

        return cls.instances
    
    
    
      