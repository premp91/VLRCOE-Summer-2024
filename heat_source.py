import openmdao.api as om


class HeatSource(om.ExplicitComponent):
    def setup(self):
        self.add_input('Q_in', val = 0.0, units = 'W')
        self.add_output('T_hot', val = 300.0, units = 'K')
    def setup_partials(self):
        self.declare_partials('*','*',method='fd')
    def compute(self,inputs,outputs):
        Q_in = inputs['Q_in']
        outputs['T_hot'] = 300.0 + Q_in * 0.01 # simplified for this case
        