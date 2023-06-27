from dataclasses import dataclass
import numpy as np
import logging

@dataclass
class Node:
    type: str
    name: str
    metadata: str
    units: str
    value: float
    id: int
    _id_counter: int = 0
    
    def __post_init__(self):
        if self.type not in ['susceptible','exposed','nutrients']:
            raise ValueError("Invalid Node type")
        Node._id_counter += 1
        self.id = Node._id_counter
            
    # list of types include susceptible, exposed, infected, decayed, recovered, phages free, phages total, washed out, resources.


@dataclass
class Connect:
    source: Node
    target: Node
    parameters: dict
    
    def connections(self,name: str):
        if self.source.type == 'nutrients' and self.source.type == 'susceptible':
            if name == 'self-growth':
                value = 1
            if name == 'type-I':
                linear_model_mult_constant = 1 if self.parameters['linear_model_mult_constant'] is None else self.parameters['linear_model_mult_constant']
                value = linear_model_mult_constant * self.source.value 
            if name == 'monod':
                half_conc = 1 if self.parameters['half_conc'] is None else self.parameters['half_conc']
                monod_mult_constant = 1 if self.parameters['monod_mult_constant'] is None else self.parameters['monod_mult_constant']
                value = monod_mult_constant * self.source.value / (half_conc + self.source.value)
        return value
        logging.debug(
            "Between {} and {} the connection used is {} with the parameters given as {}".format(
                self.source.name,self.source.target, name, self.parameters
            )
        )
    
