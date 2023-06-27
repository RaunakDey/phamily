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
        if self.type not in ['susceptible', 'exposed', 'nutrients']:
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
            logging.debug(
                "The value returned by the {} function between {} and {} for the parameters {} is {}".format(
                    name, source.type, target.type, parameters, value
                )
            )
            return value
        
        
        
        
        logging.warning(
            "The value returned by the {} function between {} and {} for the parameters {} is not applicable".format(
                name, source.type, target.type, parameters
            )
        )