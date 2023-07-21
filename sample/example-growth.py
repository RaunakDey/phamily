import logging
import sys
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


### This needs to be corrected.
sys.path.append('./../phamily/')

#More imports
from utils_func import *
from utit_plots import *
from nodes import Node, Connect

# Set up logging configuration  
logging.basicConfig(level=logging.ERROR)



ecoli = Node('susceptible', 'ecoli', value=1e4)
connection2 = Connect(ecoli,parameters_mega_list={(ecoli.type,ecoli.type):{'carrying_cap' : 70000,'growth_rate' : 0.3}})
connection2.connection_value = connection2.connections(name = 'logistic-growth')
# Initial values
initial_values = [node.value for node in Node.instances]

# Time points
time = np.arange(0, 20, 0.01)
dt = time[1] - time[0]

solution = solve_network_euler(time,initial_values)

#plt.plot(time,solution[0,:])
#plt.show()

plot_node_time_series_euler(solution,Node,time,semilog=False)