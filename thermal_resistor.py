import openmdao.api as om

class ThermalResistor(om.ExplicitComponent):
    def setup(self):
        self.add_input('T_hot', val=300.0, units='K')
        self.add_output('T_cold', val=300.0, units='K')
        self.add_input('R_th', val=1.0, units='K/W')
        self.add_input('Q_in', val=0.0, units='W')
    def setup_partials(self):
        self.declare_partials('*','*',method = 'fd')
    def compute(self,inputs,outputs):
        T_hot = inputs['T_hot']
        R_th = inputs['R_th']
        Q = inputs['Q_in']
        outputs['T_cold'] = T_hot - Q * R_th # Used for evaulating T_cold 