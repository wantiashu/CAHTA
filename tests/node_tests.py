'''
测试文件，用于检测shapes文件夹内的.py文件
'''
import sys,os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from cahta.unit_conversion import *
from cahta.shapes.tube_related import *
from cahta.property.fluid import *
from cahta.elements.SngTrbInsPp import *
from cahta import node as nd
from cahta import exceptions

dicProperty = { 'rho_kg_m3':1000.0,\
                'mu_Pas':8.9*10**(-4),\
                'lambda_W_mK':0.62,\
                'Cp_J_kgK':4187}
water = fluid(dicProperty)
node1 = nd.node("","20")
node2 = nd.node("20","20")
tube1 = tube(88.9,3.05,1000)

TR_tube = GnielinskiSngTrbInsPp(tube1, water, m3_sfm3_h(60), node1, node2)
nd.element_2nodes_handler(TR_tube,node1,node2)
print(TR_tube.direction)


#testtube.outer_heat_transfer_area



