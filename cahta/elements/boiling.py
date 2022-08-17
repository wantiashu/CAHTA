import math
#import data

deltaHv_kJ_kg = 2256.54
rhov_kg_m3 = 12.26
rhol_kg_m3 = 843.71
mu_Pas = 12.23 * 10**(-6)
lambdav_W_mK = 24.6 * 10**(-3)

class WtrNclBl(object):
    '''calculate water nucleate boiling heat transfer

    '''
  #Please Refer to Matthias Kind, Holger Martin. VDI Heat Atlas. springer. 2010
  # H2 3 Nucleate Boiling of Pure Substances
    Pc_bar = 217.7
    #参考状态，对比压力是0.1，热通量20kW/m2，加热面绝对粗糙度0.4um，
    #  水的池式沸腾传热系数为5.6kW/m2/K
    q0_kW_m2 = 20
    alpha_ref_kW_m2K = 5.6
    bcu_kWs05_mK2 = 35.35
    #

    def __init__(self, P_bar = 1, b_kWs05_mK2 = 7.73, deltaT = 5):
    # for steel, the effusivity b is 7.73, see H2 Table2
        self.b_kWs05_mK2 = b_kWs05_mK2
        self.P_bar = 1
        self.b_kWs05_mK2 = b_kWs05_mK2
        self.deltaT = deltaT

    def alpha_W_m2K(self):
        Pr = self.P_bar / self.Pc_bar
        nPr = 0.9 - 0.3 * Pr**0.5
        FPr = 1.73 * Pr**0.27 + 6.1*Pr**2 + (0.68*Pr**2)/(1-Pr**2)
        alpha_kW_m2K = (self.alpha_ref_kW_m2K)**(1/(1-nPr)) *\
                (self.deltaT/self.q0_kW_m2)**(nPr/(1-nPr)) *\
                FPr**(1/(1-nPr)) *\
                ((self.b_kWs05_mK2/self.bcu_kWs05_mK2)**0.5)**(nPr/(1-nPr))
        return alpha_kW_m2K * 1000
   
    def qcrit_kW_m2(self):
    #Please refer to 5.1 eq(26) and its explanation
    #at water's pr=0.1 
        deltaHv_kJ_kg =  1869.22
        rhov_kg_m3 = 12.26
        rhol_kg_m3 = 843.71
        sigma_N_m = 33.09 * 10**(-3)
        gra = 9.81
        K_1 = 0.13
        Pr = self.P_bar / self.Pc_bar
        qcrit0_kW_m2 = K_1 * deltaHv_kJ_kg * rhov_kg_m3**0.5 *\
                (sigma_N_m * (rhol_kg_m3-rhov_kg_m3) * gra)**0.25
        qcrit_kW_m2 = qcrit0_kW_m2 * 2.8 * Pr**0.4 * (1-Pr)
        return qcrit_kW_m2
    
class BromleyFilBl(object):
    '''caculate film boiling heat transfer coeffcient

    '''
  #Please Refer to Matthias Kind, Holger Martin. VDI Heat Atlas. springer. 2010
  # H2 5.2 Film Boiling
    #needs further working#
    def __init__(self,objFluid,tw_C = 20,tl_C = 0,P_bar = 1,Kf = 0.8):
        self.tl_C = tl_C
        self.tw_C = tw_C 
        self.Kf = Kf
        #needs further working#
        self.L_m = 0.841 * 0.9 
        self.objFluid = objFluid
        self.P_bar = P_bar
    def alphacond_W_m2K(self):
        tl_C = self.tl_C
        tw_C = self.tw_C
        tm_C = (self.tl_C + self.tw_C) /2
        P_bar = self.P_bar
        deltat_C = tw_C - tl_C
        lambdav_W_mK = self.objFluid.lambdag_W_mK(tm_C, P_bar)
        rhov_kg_m3 = self.objFluid.rhog_kg_m3(tm_C, P_bar)
        rhols_kg_m3 = self.objFluid.rhols_kg_m3(tl_C)
        hls_J_kg = self.objFluid.Hls_J_kg(tl_C)
        hv_J_kg = self.objFluid.Hg_J_kg(tm_C, P_bar)
        deltah_J_kg = - hls_J_kg + hv_J_kg
        deltarho_kg_m3 = rhols_kg_m3 - rhov_kg_m3
        etav_Pas = self.objFluid.etag_Pas(tm_C, P_bar) 
        alpha_W_m2K = self.Kf*(self.L_m*deltat_C)**(-1/4)*\
            (lambdav_W_mK**3*rhov_kg_m3*deltah_J_kg\
            *deltarho_kg_m3*9.81/etav_Pas)**(1/4)
        return alpha_W_m2K

