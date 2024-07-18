from ResistanceClassV2 import Resistance

connectivity = [
    (1, 2),
    (2, 3)
]

resistances = [1000, 3000]
num_nodes = 3
heat_input_nodes = [3]
heat_inputs = [15]
bcs = [1]
T_bcs = [0]

resistance_solver = Resistance(connectivity, resistances, num_nodes, bcs, T_bcs, heat_input_nodes, heat_inputs)
temperatures = resistance_solver.solve_thermal_network()
print("Temperatures at each node:", temperatures)
resistance_solver.visualize_network()