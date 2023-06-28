import logging
import sys
from scipy.integrate import odeint
import numpy as np

sys.path.append('./../phamily/')

from nodes import Node, Connect
#from phamily import Node, Connect

# Set up logging configuration
logging.basicConfig(level=logging.WARNING)

agar = Node('nutrients', 'agar', value=2e5)
ecoli = Node('susceptible', 'ecoli', value=1e4)
lambda_virus = Node('free_virus','lambda',value= 1e8)

connection1 = Connect(agar,ecoli)
connection1.connections(name='type-I')

connection2 = Connect(ecoli)
connection2.connections(name = 'self-growth' )

connection3 = Connect(ecoli,lambda_virus)
connection3.connections(name='infect-and-lysis' )

connection4 = Connect(lambda_virus,ecoli)
connection4.connections(name='infect-and-lysis')

## integration step

def differential_equation(state,t):
    value = 

# Set up initial conditions
initial_conditions = [agar.value, ecoli.value, lambda_virus.value]

# Set up the time span for integration
start_time = 0
end_time = 10
num_time_points = 1000
t = np.linspace(start_time, end_time, num_time_points)

# Solve the differential equations
solution = odeint(differential_equations, initial_conditions, t)