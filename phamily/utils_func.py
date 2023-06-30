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
    #for i, node in enumerate(Node.instances):
    #    print(f"{node.name} values at t=0: {initial_values[i]}")
    #    for j, time in enumerate(t):
    #        print(f"{node.name} values at t={time}: {solution[j][i]}")
    return solution


