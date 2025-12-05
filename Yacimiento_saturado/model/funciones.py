def Caudal(Pr,Pwf,Qmax):
    Qo=(1-0.2*(Pwf/Pr)-0.8*(Pwf/Pr)**2 )*Qmax
    return Qo