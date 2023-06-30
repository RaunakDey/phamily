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
                dydt[node.id-1] -= connect.connection_value
                dydt[connect.target.id-1] += connect.connection_value
        return dydt
    solution = odeint(system, initial_values, t)
    # Print the solution
    for i, node in enumerate(Node.instances):
        print(f"{node.name} values at t=0: {initial_values[i]}")
        for j, time in enumerate(t):
            print(f"{node.name} values at t={time}: {solution[j][i]}")


'''
def differential_equation(t,y):
    #t is a scalar and y is an ndarray with len(y) = y0 and function  returns  an array of the same shape as y
    dydt = y*t
    return dydt


# Set up initial conditions
initial_conditions = [agar.value, ecoli.value, lambda_virus.value]

# Set up the time span for integration
start_time = 0
end_time = 10
num_time_points = 1000
t = np.linspace(start_time, end_time, num_time_points)

# Solve the differential equations
solution = odeint(differential_equation, initial_conditions, t)
print(solution)
'''