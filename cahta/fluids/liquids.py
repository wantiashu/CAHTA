#这个作为引入物性数据的接口
#This serves as a port to physical data
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import os

curdir = os.path.dirname(__file__)


class water():
    '''
      Wolfgang Wagner, Hans-Joachim, Kretzschmar. International Steam Tables[M]. 
          second edition. springer. 1997.

    '''
    rho_kg_m3 = 998.21 #fluid dense kg/m^3
    mu_Pas = 1.002*10**(-3)#fluid dynamic viscosity Pa*s 
    Cp_J_kgK = 4185#fluid specific heat capacity J/kg/K
    lambda_W_mK = 0.598#fluid thermal_conductivity W/m/K 

    pathTbl1SatStTemp =\
        os.path.join(curdir,"data_files/IAPWS97/Tbl1SatStTemp.csv")
    pathTbl3SglPhRgn1bar =\
        os.path.join(curdir,"data_files/IAPWS97/Tbl3sglPhRgn1bar.csv")
    pathTbl3SglPhRgn01bar =\
        os.path.join(curdir,"data_files/IAPWS97/Tbl3sglPhRgn01bar.csv")

    
    def __init__(self,t_C = 20,P_bar = 1):
        #dicProperty is dictionary of properties of a fluid:
        # {'rho_kg_m3':density in kg/m^3,
        #  'mu_Pas':dynamic viscosity,
        #  'Cp_J_kgK':specific heat capacity,...}
        self.t_C = t_C
        self.P_bar = P_bar

    arrts_C= pd.read_csv(\
        os.path.join(curdir,\
        "data_files/IAPWS97/Tbl1SatStTemp.csv"),\
        usecols=["t_C"]).squeeze()
    arrHls_kJ_kg= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Tbl1SatStTemp.csv"),\
        usecols=["Hl_kJ_kg"]).squeeze()
    arrVgs_m3_kg= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Tbl1SatStTemp.csv"),\
        usecols=["vg_m3_kg"]).squeeze()
    arrVls_m3_kg= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Tbl1SatStTemp.csv"),\
        usecols=["vl_m3_kg"]).squeeze()
    arrt_C= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Table3SinglephaseRegion1bar.csv"),\
        usecols=["t_C"]).squeeze()
    arrt01bar_C = pd.read_csv(pathTbl3SglPhRgn01bar,\
        usecols=["t_C"]).squeeze()
    arrHg_kJ_kg= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Table3SinglephaseRegion1bar.csv"),\
        usecols=["Hg_kJ_kg"]).squeeze()
    arrHg01bar_kJ_kg= pd.read_csv(pathTbl3SglPhRgn01bar,\
        usecols=["Hg_kJ_kg"]).squeeze()
    arrVg_m3_kg= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Table3SinglephaseRegion1bar.csv"),\
        usecols=["vg_m3_kg"]).squeeze()
    arrVg01bar_m3_kg= pd.read_csv(pathTbl3SglPhRgn01bar,\
        usecols=["vg_m3_kg"]).squeeze()
    arrlambdag_mW_mK= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Table3SinglephaseRegion1bar.csv"),\
        usecols=["lambdav_mW_mK"]).squeeze()
    arrlambdag01bar_mW_mK= pd.read_csv(pathTbl3SglPhRgn01bar,\
        usecols=["lambdav_mW_mK"]).squeeze()
    arretag_uPas= pd.read_csv(\
        os.path.join(curdir,\
        "./data_files/IAPWS97/Table3SinglephaseRegion1bar.csv"),\
        usecols=["etav_uPas"]).squeeze()
    arretag01bar_uPas= pd.read_csv(pathTbl3SglPhRgn01bar,\
        usecols=["etav_uPas"]).squeeze()
    def rhogs_kg_m3(self, t_C = "NotProvided"):
        Vg_m3_kg = interp1d(self.arrts_C,self.arrVgs_m3_kg)
        if t_C == "NotProvided":
            return 1/Vg_m3_kg(self.t_C)
        else:
            return 1/Vg_m3_kg(t_C)
    def rhols_kg_m3(self, t_C):
        Vl_m3_kg = interp1d(self.arrts_C,self.arrVls_m3_kg)
        if t_C == "NotProvided":
            return 1/Vl_m3_kg(self.t_C)
        else:
            return 1/Vl_m3_kg(t_C)
    def rhog_kg_m3(self, t_C, P_bar = 1):
        if P_bar == 0.1:
            Vg_m3_kg = interp1d(self.arrt01bar_C,self.arrVg01bar_m3_kg)
        else:
            Vg_m3_kg = interp1d(self.arrt_C,self.arrVg_m3_kg)
        if t_C == "NotProvided":
            return 1/Vg_m3_kg(self.t_C)
        else:
            return 1/Vg_m3_kg(t_C)
    def Hls_J_kg(self, t_C):
        Hls_kJ_kg = interp1d(self.arrts_C,self.arrHls_kJ_kg)
        if t_C == "NotProvided":
            return Hls_kJ_kg(self.t_C)*1000
        else:
            return Hls_kJ_kg(t_C)*1000
    def etag_Pas(self, t_C, P_bar = 1):
        if P_bar == 0.1:
            etag_uPas = interp1d(self.arrt01bar_C,self.arretag01bar_uPas)
        else:
            etag_uPas = interp1d(self.arrt_C,self.arretag_uPas)
        if t_C == "NotProvided":
            return etag_uPas(self.t_C)*10**(-6)
        else:
            return etag_uPas(t_C)*10**(-6)
    def lambdag_W_mK(self, t_C, P_bar = 1):
        if P_bar == 0.1:
            lambdag_mW_mK = interp1d(self.arrt01bar_C,self.arrlambdag01bar_mW_mK)
        else:
            lambdag_mW_mK = interp1d(self.arrt_C,self.arrlambdag_mW_mK)
        if t_C == "NotProvided":
            return lambdag_mW_mK(self.t_C) / 1000.00 
        else:
            return lambdag_mW_mK(t_C) / 1000.00 
    def Hg_J_kg(self, t_C, P_bar = 1):
        if P_bar == 0.1:
            Hg_kJ_kg = interp1d(self.arrt01bar_C,self.arrHg01bar_kJ_kg)
        else:
            Hg_kJ_kg = interp1d(self.arrt_C,self.arrHg_kJ_kg)
        if t_C == "NotProvided":
            return Hg_kJ_kg(self.t_C) * 1000
        else:
            return Hg_kJ_kg(t_C) * 1000
