from ResistanceClass2D import Resistance

default_resistance = 10
bcs = [1]
T_bcs = [0]
heat_input_nodes = [3]
heat_inputs = [15]
lx = 1
ly = 1
nx = 5
ny = 3

rtest = Resistance(default_resistance,bcs, T_bcs, heat_input_nodes, heat_inputs,lx,ly,nx,ny)
temperatures = rtest.solve_thermal_network()
print("Temperatures at each node:", temperatures)