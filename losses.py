import openmdao.api as om

class CopperLoss(om.ExplicitComponent):
    def setup(self):
        self.add_input('I', val=0.0, units='A')  # Current in Amperes
        self.add_input('R_cu', val=0.0, units='ohm')  # Resistance in ohms
        self.add_output('P_loss', val=0.0, units='W')  # Power loss in Watts

    def setup_partials(self):
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        I = inputs['I']
        R_cu = inputs['R_cu']
        outputs['P_loss'] = I ** 2 * R_cu
