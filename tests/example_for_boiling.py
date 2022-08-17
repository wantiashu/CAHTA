'''
测试文件，用于检测shapes文件夹内的.py文件
'''
import sys,os
import numpy
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from cahta.unit_conversion import *
from cahta.shapes.tube_related import *
from cahta.fluids import liquids
from cahta.elements.boiling import *

A_m2 = 1.5

objWater = liquids.water(100,1)
print(objWater.rhogs_kg_m3())
print(objWater.rhogs_kg_m3(120))

objFilmBoiling = BromleyFilBl(objWater,200,100,1)
objFilmBoiling01 = BromleyFilBl(objWater,200,100,0.1)
objNucBoiling = WtrNclBl(deltaT = 25)
array = []
for t_C in range(101,128):
    objNucBoiling.deltaT = t_C - 100
    array.append([t_C, 0.94 * objNucBoiling.alpha_W_m2K(),\
        0.94 * objNucBoiling.deltaT * A_m2 * objNucBoiling.alpha_W_m2K() / 1000])
for t_C in range(128,300):
    deltaT = t_C - 100
    objFilmBoiling.tw_C = t_C
    array.append([t_C, objFilmBoiling.alphacond_W_m2K(),\
        deltaT * A_m2 * objFilmBoiling.alphacond_W_m2K() / 1000])
nparr = numpy.asarray(array)
numpy.savetxt("1barboling.csv", nparr, delimiter=",")
#print(array)

print (objFilmBoiling.alphacond_W_m2K())
print (objFilmBoiling01.alphacond_W_m2K())
print (objNucBoiling.alpha_W_m2K())
