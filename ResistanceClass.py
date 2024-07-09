from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import schemdraw
import schemdraw.elements as elm

class Resistance:
    def __init__(self, connectivity, resistances, num_nodes):
        self.connectivity = connectivity
        self.resistances = resistances
        self.num_nodes = num_nodes
        self.R = self.assemble_resistance_matrix()

        # for node in bcs:
        #   if node is in heat_input_nodes:
        #       raise ValueError("Cannot have overlap between bcs and externally apploied loads")
    
    def assemble_resistance_matrix(self):
        # Initialize global resistance matrix to zeros
        R = np.zeros((self.num_nodes, self.num_nodes))

        # Assemble global resistance matrix using connectivity array
        for i, (n1, n2) in enumerate(self.connectivity):
            Rth = self.resistances[i]
            #G = 1 / Rth  # Conductance
            G =  Rth  # Conductance
            # Adding conductance to the global resistance matrix
            R[n1-1, n1-1] += G
            R[n2-1, n2-1] += G
            R[n1-1, n2-1] -= G
            R[n2-1, n1-1] -= G
            print('R matrix:\n', R)
        
        return R

    def apply_boundary_conditions(self, Q, bcs):
        n = len(Q)
        reduced = np.setdiff1d(np.arange(stop=n), bcs)
        q_reduced = Q[reduced]
        R_reduced = self.R[reduced, :]
        R_reduced = R_reduced[:, reduced]

        return R_reduced, q_reduced, reduced

    def solve_thermal_network(self, heat_inputs, bcs, T_bcs):
        # Convert the heat inputs list to a numpy array
        Q = np.array(heat_inputs)

        R_reduced, Q_reduced, reduced = self.apply_boundary_conditions(Q, bcs)

        try:
            T_reduced = np.linalg.solve(R_reduced, Q_reduced)
        except np.linalg.LinAlgError:
            print("Singular matrix encountered. The system may be underconstrained or overconstrained.")
            return None

        T = self.assemble_global_solution(self.num_nodes, reduced, T_reduced, T_bcs, bcs)

        return T

    def assemble_global_solution(self, nnodes, reduced, T_reduced, T_bcs, bcs):
        T = np.zeros(nnodes)
        T[reduced] = T_reduced
        T[bcs] = T_bcs

        return T
    
    def visualize_network(self):
        with schemdraw.Drawing() as d:
            node_positions = {}
            parallel_offsets = defaultdict(int)
            x = 0
            y = 0

            # Place nodes in a straight line
            for i in range(1, self.num_nodes + 1):
                node_positions[i] = (x, y)
                d += elm.Dot().at((x, y)).label(str(i), loc='bottom')
                x += 2  # Move to the right for the next node

            # Draw resistors
            for i, (n1, n2) in enumerate(self.connectivity):
                Rth = self.resistances[i]
                offset = parallel_offsets[(n1, n2)] * 0.5
                if parallel_offsets[(n1, n2)] == 0:
                    d += (elm.Resistor().at(node_positions[n1])
                          .to(node_positions[n2]).label(f'R={Rth}', loc='bottom'))
                else:
                    d += (elm.Resistor().at((node_positions[n1][0], node_positions[n1][1] + offset))
                          .to((node_positions[n2][0], node_positions[n2][1] + offset)).label(f'R={Rth}', loc='bottom'))
                parallel_offsets[(n1, n2)] += 1


if __name__ == '__main__':
    # Example usage
    connectivity = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (1, 3)
    ]

    resistances = [1, 2, 3, 4, 4]  # Thermal resistances of the elements
    heat_inputs = [10, 0, 0, 0, 0]  # Heat input at each node
    num_nodes = 5  # Total number of nodes
    bcs = [4]
    T_bcs = [10] 

    # Create an instance of the Resistance class
    resistance_solver = Resistance(connectivity, resistances, num_nodes)

    # Solve for the temperature distribution
    temperatures = resistance_solver.solve_thermal_network(heat_inputs, bcs, T_bcs)

    print("Temperatures at each node:", temperatures)
