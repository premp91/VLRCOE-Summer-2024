from ResistanceClassV2 import Resistance

connectivity = [(0, 4), (0, 1), (1, 5), (1, 2), (2, 6), (2, 3), (3, 7), (4, 8), (4, 5), (5, 9), (5, 6), (6, 10), (6, 7), (7, 11), (8, 9), (9, 10), (10, 11)]

resistances = len(connectivity)*[10]
num_nodes = 12
heat_input_nodes = [3]
heat_inputs = [15]
bcs = [1]
T_bcs = [0]

resistance_solver = Resistance(connectivity, resistances, num_nodes, bcs, T_bcs, heat_input_nodes, heat_inputs)
temperatures = resistance_solver.solve_thermal_network()
print("Temperatures at each node:", temperatures)
resistance_solver.visualize_network()