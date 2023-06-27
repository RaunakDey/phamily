import logging
import sys

sys.path.append('./../src/')

from nodes import Node, Connect

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

agar = Node('nutrients', 'agar', value=2.0)
ecoli = Node('susceptible', 'ecoli', value=1)

connection1 = Connect(agar,ecoli)

connection1.parameters_mega_list = {
    ('nutrients', 'susceptible'): {
        'linear_model_mult_constant': 0.5,
        'half_conc': 0.5,
        'monod_mult_constant': 0.5
    }
}
connection1.connections(name='type-I')

