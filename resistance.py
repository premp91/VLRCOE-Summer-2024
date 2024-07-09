import numpy as np


def assemble_resistance_matrix(connectivity, resistances, num_nodes):
    # initialize global resistance matrix to zeros
    R = np.zeros((num_nodes,num_nodes))

    # Assemble global resistance matrix using connectivity array
    for i, (n1, n2) in enumerate(connectivity):
        Rth = resistances[i]
        G = 1 / Rth  # Conductance
        # Adding conductance to the global resistance matrix
        R[n1-1, n1-1] += G
        R[n2-1, n2-1] += G
        R[n1-1, n2-1] -= G
        R[n2-1, n1-1] -= G
        print('R matrix:\n',R)
   
    return R

def apply_boundary_conditions(R, Q, bcs):
    
    n = len(Q)
    reduced = np.setdiff1d(np.arange(stop=n),bcs)
    q_reduced = Q[reduced]
    R_reduced = R[reduced,:]
    R_reduced = R_reduced[:,reduced]

    # print('Q vector:\n',Q)
    return R_reduced, q_reduced , reduced

def solve_thermal_network(connectivity,resistances,heat_inputs,num_nodes, bcs, T_bcs):

    R = assemble_resistance_matrix(connectivity, resistances, num_nodes)

    # Convert the heat inputs list to a numpy array
    Q = np.array(heat_inputs)

    R_reduced, Q_reduced, reduced = apply_boundary_conditions(R, Q, bcs)
    

    try:
        T_reduced = np.linalg.solve(R_reduced, Q_reduced)
    except np.linalg.LinAlgError:
        print("Singular matrix encountered. The system may be underconstrained or overconstrained.")
        return None

    T = assemble_global_solution(num_nodes, reduced , T_reduced , T_bcs , bcs)

    return T

def assemble_global_solution(nnodes , reduced, T_reduced, T_bcs, bcs):

    T = np.zeros(nnodes)
    T[reduced] = T_reduced
    T[bcs] = T_bcs

    return T

# Example inputs
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

# Solve for the temperature distribution
temperatures = solve_thermal_network(connectivity, resistances, heat_inputs, num_nodes,bcs,T_bcs)

print("Temperatures at each node:", temperatures)

