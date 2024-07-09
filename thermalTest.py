import openmdao.api as om
from heat_source import HeatSource
from heat_sink import HeatSink
from thermal_resistor import ThermalResistor


prob = om.Problem()

# Subsystems
prob.model.add_subsystem('heat_source', HeatSource(), promotes_inputs=['Q_in'], promotes_outputs=['T_hot']) 
prob.model.add_subsystem('thermal_resistor', ThermalResistor(), promotes_inputs=['T_hot', 'R_th', 'Q_in'], promotes_outputs=['T_cold'])
prob.model.add_subsystem('heat_sink', HeatSink(), promotes_inputs=['T_cold'], promotes_outputs=['Q_out'])

# Connections
prob.model.connect('heat_source.T_hot', [])
prob.model.connect('thermal_resistor.T_cold', [])
prob.model.connect('heat_source.Q_in', [])


prob.setup()

# Set input values
prob.set_val('Q_in', 100.0)  # Input power in Watts
prob.set_val('R_th', 0.5)    # Thermal resistance in K/W

# Run the model
prob.run_model()

# Get + print outputs
#print(prob.get_val('heat_source.T_hot'))

print('T_hot:', prob.get_val('T_hot'))
print('T_cold:', prob.get_val('T_cold'))
print('Q_out:', prob.get_val('Q_out'))
