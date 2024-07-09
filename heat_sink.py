import openmdao.api as om

class HeatSink(om.ExplicitComponent):
    def setup(self):
        self.add_input('T_cold', val=300.0, units='K')
        self.add_output('Q_out', val=0.0, units='W')

    def setup_partials(self):
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        T_cold = inputs['T_cold']
        outputs['Q_out'] = (T_cold - 300.0) * 0.1  # Simplified linear relation

        
