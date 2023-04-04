import numpy as np
from lib.sql_browse import SQL_requestions
import json

class Heandler:
    
    def __init__(self):
        self.Params = []
    def models(self):
        self.SQL = SQL_requestions('db/db.sqlite3')
        """
            Запрашиваем модели генераторов из базы

        """
        j_dump = json.dumps(self.SQL.request(request_type= 'SELECT',
                        Table_name= 'FROM SinchroGenerators',
                        Variable= 'NAME'))
        j_file = json.loads(j_dump)

        for i in j_file[0]:
            j_file[0][j_file[0].index(i)] = i.replace('_','-')

        return j_file
    

    def SQL_variables(self, model:str = None):
        self.SQL = SQL_requestions('db/db.sqlite3')
        if model is not None:

            model = model.replace('-','_')
            
            self.Params = json.dumps(self.SQL.request(request_type= 'SELECT',
                            Table_name= f"FROM MechParams INNER JOIN RESISTANCE,SinchroGenerators,TimeConstants",
                            Variable= '*',
                            Condition= "WHERE",
                            arg=('MechParams.Name','=',f"'{model}'")))
            
            self.Params = json.loads(self.Params)[0]

            del self.Params[0]          ##0,4,15,22
            del self.Params[4-1]
            del self.Params[15-2]
            del self.Params[22-3]

            # print(self.Params)

    def Variable_determinate(self):
        
        # Механические параметры
        self.GD2r:float              = float(self.Params[0])  # 14.9
        self.GD2t:float              = float(self.Params[1])  # 14.9
        self.n:int                   = float(self.Params[2])  # 3000
        # Сопротивления
        self.x_sigma:float           = float(self.Params[3])  # 0.148
        self.xd:float                = float(self.Params[4])  # 1.7
        self.x1d:float               = float(self.Params[5])  # 0.26
        self.x2d:float               = float(self.Params[6])  # 0.173
        self.xq:float                = float(self.Params[7])  # 1.69
        self.x1q:float               = float(self.Params[8])  # 0
        self.x2q:float               = float(self.Params[9])  # 0.18
        self.x2:float                = float(self.Params[10]) # 0.211
        self.x0:float                = float(self.Params[11]) # 0.088
        self.Ra:float                = float(self.Params[12]) # 0.00118
        # О синхронном генераторе
        self.NomFullPower:float      = float(self.Params[13]) # 353
        self.NomActPower:float       = float(self.Params[14]) # 300
        self.NomStatorVoltage:float  = float(self.Params[15]) # 20
        self.NomStatorCurrent:float  = float(self.Params[16]) # 10.2
        self.cosfi:float             = float(self.Params[17]) # 0.85
        self.NomFrec:float           = float(self.Params[18]) # 50
        # Постоянные времени
        self.T1d0:float              = float(self.Params[19]) # 5.9
        self.T2d0:float              = float(self.Params[20]) # 0.168
        self.T1q0:float              = float(self.Params[21]) # 0.0
        self.T2q0:float              = float(self.Params[22]) # 0.5
            

class Solver(Heandler):

    def __init__(self, DEBUG = False):
        super().__init__()
        
        
    def main(self, IndRes = 0, BasePower = 0, BaseVoltage = 0, kzTime = 0, DEBUG = False):
        
        try:

            self.InductiveResistance    = IndRes            # Внешнее сопротивление сети (эквивалентное, о.е)
            self.BasePower              = BasePower         # Базисная мощность сети ступени КЗ
            self.BaseVoltage            = BaseVoltage       # Базисное напряжение сети ступени КЗ
            self.kz_Time                = kzTime
            self.DEBUG                  = DEBUG


            Xout        = float(self.InductiveResistance)
            BasePower   = float(self.BasePower)
            BaseVoltage = float(self.BaseVoltage)
            kzTime      = int(str(self.kz_Time).split('0.')[1])
            print(kzTime)
            S_BASE = BasePower * 10**6                      # Базисная мощность
            U_BASE = BaseVoltage * 10**3                    # Базисное напряжение
            I_BASE = S_BASE/(np.sqrt(3)*U_BASE)             # Базисный ток

            I_0 = (0.7*self.NomFullPower*10**6)/(np.sqrt(3)*self.NomStatorVoltage*10**3) #Ток режима работы
            sinfi = np.sqrt(1- self.cosfi**2)
            
            R = self.NomStatorVoltage*10**3/I_0  # Активное сопротивелние Ом

            U0b = self.NomStatorVoltage*10**3 / U_BASE
            I0b = 1

            Q0   = np.sqrt((0.7*self.NomFullPower**2 - 0.7*self.NomActPower**2)*10**12)    # Реактивная мощность
            Qnom = np.sqrt((self.NomFullPower**2 - self.NomActPower**2)*10**12)

            Xd  = self.xd  * (U_BASE**2/(self.NomFullPower*10**6))
            Xq  = self.xq  * (U_BASE**2/(self.NomFullPower*10**6))
            X2d = self.x2d * (U_BASE**2/(self.NomFullPower*10**6))
            X1d = self.x1d * (U_BASE**2/(self.NomFullPower*10**6))

            E11d = np.sqrt((U0b*self.cosfi)**2 + (U0b*sinfi + I0b*X2d)**2)

            T_sigma = self.x_sigma/(2*3.14*50*self.Ra)


            Eq = (U_BASE**4 + Qnom*U_BASE**2*(Xd + Xq) + (self.NomActPower**2*10**12 + Qnom**2)*Xd*Xq)/(U_BASE*np.sqrt(U_BASE**4 + 2*Qnom*U_BASE**2*Xq + (self.NomActPower**2*10**12 + Qnom**2)*Xq**2))
            E11q0 = np.sqrt((U0b + (I0b)*X2d*sinfi)**2 + ((I0b)*X2d*self.cosfi)**2)
            E1q0 = np.sqrt((U0b + (I0b)*X1d*sinfi)**2 + ((I0b)*X1d*self.cosfi)**2)
            

            Eq0   = Eq/U_BASE
            # E11q0 = E11q/U_BASE
            # E1q0  = E1q/U_BASE

            t = [float(i) for i in np.arange(0.00,0.51, 0.01)] # Интервал и шаг времени

            def Ldpt(t = t,Eq0 = Eq0, Xd =Xd, Xout = Xout, 
                        E1q0 = E1q0, X1d = X1d, T1d0 = self.T1d0, 
                        T11d0 = self.T2d0, E11q0=E11q0, X11d = X2d, Tsigma = T_sigma):
                
                Eqp = 3  # Предельное значение ЭДС
                idpt = []

                for t in t:
                    idpt_1 = (Eq0/(Xd + Xout) + (E1q0/(X1d + Xout) - Eq0/(Xout+Xd))*np.exp(-t/T1d0))
                    idpt_2 = (E11q0/(X11d + Xout) - E1q0/(Xout+X1d))*np.exp(-t/T11d0)
                    idpt_3 = (Eqp - Eq0/(Xd+Xout))*(((1-(T1d0-Tsigma)/(T1d0 - T11d0))*np.exp(-t/T1d0))  + ((T11d0 - Tsigma)/(T1d0-T11d0))*np.exp(-t/T11d0))
                    SUM = idpt_1 + idpt_2 + idpt_3
                    idpt.append(SUM)

                return idpt

            IDPT = Ldpt()

            def Iqpt(t=t, E11d = E11d, X11q = self.x2q, Xout = Xout, T11q0 = self.T2q0):
                iqpt = []
                for t in t:
                    iqpt_1 = (E11d/(X11q + Xout)*np.exp(-t/T11q0))
                    iqpt.append(iqpt_1)
                
                return iqpt

            IQPT = Iqpt()

            def Ipt(IQPT = IQPT, IDPT= IDPT):
                IPT = []
                for i,j in zip(IDPT, IQPT):
                    IPT.append(np.sqrt(i**2 + j**2))
                return IPT
            
            IPT = Ipt()

            def Gamma(Ipt = IPT, Ub = U_BASE, Sb = S_BASE):
                GAMMA = []
                for i in Ipt:
                    gamma = ((i/Ipt[0]))
                    GAMMA.append(gamma)
                    
                return GAMMA
            
            _gamma = Gamma()
            I_kz = _gamma[kzTime]

            if self.DEBUG == True:
                variable_dict = {

                    'I 0': I_0,     # ok
                    'sinfi':sinfi,  # ok
                    'R':R,          # ok
                    'U0b':U0b,      # ok
                    'I0b':I0b,      # ok
                    'Q0':Q0,        # ~
                    'Qnom':Qnom,    # ok
                    'Xd':Xd,        # ok
                    'Xq':Xq,        # ok
                    'X2d':X2d,      # ok
                    'X1d':X1d,      # ok
                    "E''d":E11d,    # ok
                    "E'q0":E1q0,      # ok
                    "E''q0":E11q0,    # ok
                    "Eq":Eq,        # ok
                    "Tsigma":T_sigma, # ok
                    "_gamma":_gamma
                    
                }

                for i,j in zip(variable_dict.keys(),variable_dict.values()):
                    print(i,':',j)
                    print('----------------')

            return [_gamma,'',I_kz]
        except ZeroDivisionError:
            return [0,'Ошибка деления на 0. Заполните все поля формы.']
        except IndexError:
            return [0, 'Ошибка в формате поля расчётного времени кз. Введите в формате 0.00']

