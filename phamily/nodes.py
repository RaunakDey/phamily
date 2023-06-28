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
    id: int = None
    _id_counter: int = 0
    
    '''
    creates new ids for new nodes.
    '''
    def __post_init__(self):
        ### add list of nodes above this
        if self.type not in ['susceptible', 'free_virus', 'nutrients']:
            raise ValueError("Invalid Node type")
        Node._id_counter += 1
        self.id = Node._id_counter


@dataclass
class Connect:
    source: Node = None
    target: Node = None
    parameters_mega_list: dict = None
    
    '''
    if there is no target, it selects the source as the target 
    '''
    
    def __post_init__(self):
        self.target = self.source if self.target is None else self.target

    def connections(self, name: str):
        source = self.source
        target = self.target if self.target is not None else self.source
        key = (source.type, target.type)
        parameters = self.parameters_mega_list.get(key, {}) if self.parameters_mega_list else {}

        #### Can use mapping and lambda function to optimize this
        
        if source.type == 'nutrients' and target.type == 'susceptible':
            default_parameters = {
                'linear_model_mult_constant': 1,
                'half_conc': 1,
                'monod_mult_constant': 1
            }
            parameters = {**default_parameters, **parameters}

            if name == 'self-growth':
                value = 1
            elif name == 'type-I':
                linear_model_mult_constant = parameters['linear_model_mult_constant']
                value = linear_model_mult_constant * self.source.value
            elif name == 'monod':
                half_conc = parameters['half_conc']
                monod_mult_constant = parameters['monod_mult_constant']
                value = monod_mult_constant * self.source.value / (half_conc + self.source.value)
            else:
                raise NameError('wrong name of function')
            
        
        elif source.type == 'nutrients' and target.type == 'nutrients':
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
                'linear_model_mult_constant': 1,
                'half_conc': 1,
                'monod_mult_constant': 1,
                'carrying_cap' : 1e4,
                'outflow_rate' : 1
            }
            parameters = {**default_parameters, **parameters}

            if name == 'self-growth':
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
                'adsorption_rate' : 1e-10,
            } 
            parameters = {**default_parameters, **parameters}
            if name == 'infect-and-lysis':
                adsorption_rate = parameters['adsorption_rate']
                value = -adsorption_rate*source.value*target.value
            else:
                raise NameError('wrong name of function')
            
        elif source.type == 'free_virus' and target.type == 'susceptible':
            default_parameters = {
                'adsorption_rate' : 1e-10,
                'burst_size' : 100
            } 
            parameters = {**default_parameters, **parameters}
            if name == 'infect-and-lysis':
                adsorption_rate = parameters['adsorption_rate']
                burst_size = parameters['burst_size']
                value = burst_size*adsorption_rate*source.value*target.value
            else:
                raise NameError('wrong name of function')
        
        ### Just add lines above this
        logging.debug(
                "The value returned by the {} function between {} and {} for the parameters {} is {}".format(
                    name, source.type, target.type, parameters, value
                )
            )
        return value   
    
    def add_connections(self):
        raise NotImplemented
    
    
      