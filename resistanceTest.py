from ResistanceClass import Resistance


connectivity = [
    (1, 2),
    (2, 3)
]

resistances = [1000, 3000]  # Thermal resistances of the elements
heat_inputs = [-15, 0, 15]  # Heat input at each node
num_nodes = 3  # Total number of nodes
bcs = [0]
T_bcs = [0]

# heat_inputs = (200,)
# heat_inputs = [-15, 0, 15, 0, 15, 2, ...]

# heat_inputs_nodes = [0, 10, 100, 199]
# heat_inptus = [-15, 15, 10, 2]

# Create an instance of the Resistance class
resistance_solver = Resistance(connectivity, resistances, num_nodes)

# Solve for the temperature distribution
temperatures = resistance_solver.solve_thermal_network(heat_inputs, bcs, T_bcs)

print("Temperatures at each node:", temperatures)
resistance_solver.visualize_network()