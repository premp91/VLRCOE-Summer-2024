import numpy as np
import matplotlib.pyplot as plt
from ConnectivityMap2D import Resistance2D 

class Resistance:
    def __init__(self, num_nodes, default_resistance,bcs, T_bcs, heat_input_nodes, heat_inputs,lx,ly,nx,ny):
        connectivity_solver = Resistance2D(lx,ly,nx,ny)

        self.connectivity = connectivity_solver.assemble_connectivity()
        self.resistances = len(self.connectivity)*[default_resistance]
        self.num_nodes = num_nodes
        self.bcs = [x - 1 for x in bcs]
        self.heat_input_nodes = heat_input_nodes
        self.heat_inputs = heat_inputs
        self.T_bcs = T_bcs
        self.R = self.assemble_resistance_matrix()

        # Checks for overlap in bcs and heat input nodes
        for node in bcs:
           if node in heat_input_nodes:
               raise ValueError("Cannot have overlap between bcs and externally applied loads")
           
    def assemble_resistance_matrix(self):
        # Initialize global resistance matrix to zeros
        R = np.zeros((self.num_nodes, self.num_nodes))

        # Assemble global resistance matrix using connectivity array
        for i, (n1, n2) in enumerate(self.connectivity):
            Rth = self.resistances[i]
            G = 1 / Rth  # Conductance
            #G =  Rth  # Resistance
            # Adding conductance to the global resistance matrix
            R[n1-1, n1-1] += G
            R[n2-1, n2-1] += G
            R[n1-1, n2-1] -= G
            R[n2-1, n1-1] -= G
            #print('R matrix:\n', R)
        print('R matrix:\n', R)
        
        return R

    def apply_boundary_conditions(self, Q, bcs):
        n = len(Q)
        #bcs = [x - 1 for x in bcs]
        reduced = np.setdiff1d(np.arange(stop=n), bcs)
        q_reduced = Q[reduced]
        R_reduced = self.R[reduced, :]
        R_reduced = R_reduced[:, reduced]

        return R_reduced, q_reduced, reduced

    def solve_thermal_network(self):
        # Apply the heat input nodes and inputs to assemble a full heat array for RT=Q

        Q = np.zeros(self.num_nodes)
        self.heat_input_nodes = [x - 1 for x in self.heat_input_nodes]
        Q[self.heat_input_nodes] = self.heat_inputs
        #print(Q)
        # Q = np.array(heat_inputs)

        R_reduced, Q_reduced, reduced = self.apply_boundary_conditions(Q, self.bcs)

        try:
            T_reduced = np.linalg.solve(R_reduced, Q_reduced)
        except np.linalg.LinAlgError:
            print("Singular matrix encountered. The system may be underconstrained or overconstrained.")
            return None

        T = self.assemble_global_solution(self.num_nodes, reduced, T_reduced, self.T_bcs, self.bcs)

        return T

    def assemble_global_solution(self, nnodes, reduced, T_reduced, T_bcs, bcs):
        T = np.zeros(nnodes)
        T[reduced] = T_reduced
        T[bcs] = T_bcs

        return T