
class node:
   '''Node connecting heat resistant elements

   '''
   def __init__(self,T_C,Q_kW):
       self.T_C = T_C
       self.Q_kW = Q_kW

def element_2nodes_handler(ele,node1,node2):
    '''define the task for this element

           node1(T1,Q1),node2(T2,Q2)
            T1      T2      Q1         Q2     return     input    output/overide
           ---------------------------------------------------------------------
           any      any   !=""&!=Q2   !=""    any                 heat unbalance
           !=""    !=""    !=""       any     any                 over rigid  
            =""     =T1     any       any     any                 no temp diff
           !=""     =""     =""        =""    any                 insuff input 
            =""    !=""     =""        =""    any                 insuff input 
            >T2    !=""     =""        =""    heating    T1,T2    Q1,Q2=Q1
            <T2    !=""     =""        =""    cooling    T1,T2    Q1,Q2=Q1
           !=""     =""    !=""        =""    ""         T1,Q1    Q2=Q1,T2    
           !=""     =""     =""       !=""    ""         T1,Q2    Q1=Q2,T2    
            >T2    !=""    !=""        =""    heating    T1,Q1    Q1=Q2,T2    
            >T2    !=""     =""       !=""    heating    T1,Q2    Q1=Q2,T2    
            <T2    !=""    !=""        =""    cooling    T1,Q1    Q1=Q2,T2    
            <T2    !=""     =""       !=""    cooling    T1,Q2    Q1=Q2,T2    
        '''
#rule out four exceptions
    if node1.Q_kW != node2.Q_kW \
        and node1.Q_kW != "" and node2.Q_kW != "":
        raise InvalidNodeError("heat unbalance") 
    if node1.T_C == node2.T_C :
        raise InvalidNodeError("no temperature difference")
    if node1.Q_kW == "" and node2.Q_kW == "" :
        pass
    elif node1.T_C != "" and node2.T_C != "" :
        raise InvalidNodeError("over rigid")
    if node1.T_C != "" and node2.T_C == "" \
            and node1.Q_kW == "" and node2.Q_kW == "" :
                raise InvalidNodeError("insufficient input")
    if node1.T_C == "" and node2.T_C != "" \
            and node1.Q_kW == "" and node2.Q_kW == "" :
                raise InvalidNodeError("insufficient input")

    # a special case where only temperatures are set
    if node1.Q_kW == "" and node2.Q_kW == "" :
        pass
    else:
        #set Q
        if node1.Q_kW != "" and node2.Q_kW == "" :
            node2.Q_kW == node1.Q_kW
        elif node2.Q_kW != "" and node1.Q_kW == "" :
            node1.Q_kW == node2.Q_kW
    
    #return
    if node1.T_C == "" and node2.T_C != "" :
       ele.direction =  "cooling"
    elif node1.T_C != "" and node2.T_C == "" :
       ele.direction =  "heating"
    elif node1.T_C > node2.T_C :
       ele.direction =  "heating"
    else:
       ele.direction =  "cooling"
