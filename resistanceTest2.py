from ResistanceClassV2 import Resistance

connectivity = [(1, 7), (1, 2), (2, 8), (2, 3), (3, 9), (3, 4), (4, 10), (4, 5), (5, 11), (5, 6), (6, 12), (7, 13), (7, 8), (8, 14), (8, 9), (9, 15), (9, 10), (10, 16), (10, 11), (11, 17), (11, 12), (12, 18), (13, 19), (13, 14), (14, 20), (14, 15), (15, 21), (15, 16), (16, 22), (16, 17), (17, 23), (17, 18), (18, 24), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24)]

resistances = len(connectivity)*[10]
num_nodes = 24
heat_input_nodes = [3]
heat_inputs = [15]
bcs = [1]
T_bcs = [0]

resistance_solver = Resistance(connectivity, resistances, num_nodes, bcs, T_bcs, heat_input_nodes, heat_inputs)
temperatures = resistance_solver.solve_thermal_network()
print("Temperatures at each node:", temperatures)
resistance_solver.visualize_network()