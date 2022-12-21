'''Collection of single phase turbulent heat transfer and thermal resistance

'''
import math
#The following py must be imported
from cahta.unit_conversion import *
from cahta.node import *
from cahta.exceptions import *

#Gnielinski
class GnielinskiSngTrbInsPp(object):
    '''caculate in tube turbulent flow heat transfer coefficient
    
    
    '''
  #Please Refer to HEDH 1983 2.5.1 (41)    

    def __init__(self,objTube,objFluid, V_m3_s,
            node1 = node.node(25,0),
            node2 = node.node(25,0),
            direction = "heating"):
    # objTube is an instance of class tube
    # objFluid is an instance of class fluid
        self.V_m3_s=V_m3_s
        self.objTube=objTube
        self.objFluid=objFluid
        self.node1=node1
        self.node2=node2
        #self.node_initializer(node1,node2)
        self.

    # Find the task
    

    # Fluid Velocity
    def u_m_s(self):
        return self.V_m3_s/m2fmm2(self.objTube.St_mm2)
    # Renolds Number dimensionless
    def Re_1(self):
        return self.objFluid.rho_kg_m3 * \
              self.u_m_s() * \
              mfmm(self.objTube.Dti_mm) / \
              self.objFluid.mu_Pas
    # Prandl Number
    def Pr_1(self):
         return self.objFluid.Cp_J_kgK * \
                self.objFluid.mu_Pas / \
                self.objFluid.lambda_W_mK
  # Friction factor
    def f_1(self):
         return ( 1.82 * math.log10(self.Re_1()) - 1.64 ) ** (-2)
  # Nusselt Number
    def Nu_1(self):
         return self.f_1()/8*(self.Re_1()-1000)*self.Pr_1() / \
                  ( 1.0 + 1.27 * (self.f_1())**0.5 * \
                  ( self.Pr_1() ** (2/3) -1 ) ) *\
                  ( 1.0 + \
                  (self.objTube.Dti_mm / self.objTube.Lt_mm) ** \
                  (2/3) )
  # Heat transfer rate
    def alpha_W_m2K(self):
        return self.Nu_1() * \
              self.objFluid.lambda_W_mK / \
              mfmm(self.objTube.Dti_mm)
  # Heat Resistence
    def r_m2K_W(self):
        return 1.0 / self.alpha_W_m2K()
