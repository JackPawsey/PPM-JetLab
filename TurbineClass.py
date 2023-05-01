#Imports
import math
import SettingsClass

#Inputs: Intake Velocity, Mass Flow Rate, Pressure Ratio, Compressor Eff, Turbine Eff
class GasTurbine:
    def __init__(self, Va, MFR, CPR, NPC, NPT):

        #Kinetic Energy variables
        self.KEaJ = 0
        self.KEaKJKG = 0
        self.KEbJ = 0
        self.KEbKJKG = 0

        #Pressure Ratio
        self.CPR = CPR

        #Compressor/Turbine Efficiency
        self.NPC = NPC
        self.NPT = NPT

        #Temperatures
        self.Ta = SettingsClass.settings.config_list[3]
        self.T1 = 0
        self.T2s = 0
        self.T2a = 0
        self.T3 = SettingsClass.settings.config_list[5]
        self.T4s = 0
        self.T4a = 0
        self.Tb = 0

        #Pressures
        self.Pa = SettingsClass.settings.config_list[4]
        self.P1 = 0
        self.P2 = 0
        self.P3 = 0
        self.P4 = 0
        self.Pb = SettingsClass.settings.config_list[4]

        #Air velocities
        self.Va = Va
        self.Vb = 0

        #Mass Flow Rate
        self.MFR = MFR

        #Engine Thrust
        self.thrust = 0

    #Calculate input kinetic energy
    def cal_KEaJ(self):
        self.KEaJ = 0.5 * self.MFR * self.Va**2

    #Convert J to KJ/KG
    def conv_to_KEaKJKG(self):
        self.KEaKJKG = self.KEaJ / self.MFR / 1000

    #Calculate temperature at 1
    def cal_T1(self):
        self.T1 = self.Ta + (self.KEaKJKG / SettingsClass.settings.config_list[7])

    #Calculate pressure at 1
    def cal_P1(self):
        self.P1 = ((self.T1 / self.Ta)**(SettingsClass.settings.config_list[6] / (SettingsClass.settings.config_list[6] - 1))) * self.Pa

    #Calculate pressure at 2
    def cal_P2(self):
        self.P2 = self.P1 * self.CPR

    #Calculate pressure at 3
    def cal_P3(self):
        self.P3 = self.P2 * ((100 - SettingsClass.settings.config_list[2]) / 100)

    #Calculate temperature at 2s
    def cal_T2s(self):
        self.T2s = self.T1 * (self.P2 / self.P1)**((SettingsClass.settings.config_list[6] - 1) / SettingsClass.settings.config_list[6])

    #Calculate temperature at 2a
    def cal_T2a(self):
        self.T2a = self.T1 + ((1 / (self.NPC / 100)) * (self.T2s - self.T1))

    #Calculate temperature at 4a
    def cal_T4a(self):
        self.T4a = self.T3 - (self.T2a - self.T1)

    #Calculate temperature at 4s
    def cal_T4s(self):
        self.T4s = self.T3 - ((self.T3 - self.T4a) / (self.NPT / 100))

    #Calculate pressure at 4
    def cal_P4(self):
        temp = self.P3 * (self.T4s / self.T3)**(SettingsClass.settings.config_list[6] / (SettingsClass.settings.config_list[6] - 1))
        try:
            if (temp > -100000):
                self.P4 = temp
        except:
            print("Value too small to handle...")

    #Account for pressure loss in jetpipe
    def cal_jetpipe_pressure_loss(self):
        self.P4 = self.P4 * ((100 - SettingsClass.settings.config_list[2]) / 100)

    #Calculate output temperature
    def cal_Tb(self):
        self.Tb = self.T4a * (self.Pb / self.P4)**((SettingsClass.settings.config_list[6] - 1) / SettingsClass.settings.config_list[6])

    #Calculate output kinetic energy
    def cal_KEbKJKG(self):
        if (self.T4a <= 0 and self.Tb <= 0):
            print("Negative values adding to positive value...")
        else:
            self.KEbKJKG = SettingsClass.settings.config_list[7] * (self.T4a - self.Tb)

    #Convert KJ/KG to J
    def conv_to_KEbJ(self):
        self.KEbJ = self.KEbKJKG * self.MFR * 1000
        if (self.KEbJ < 0):
            self.KEbJ = 0
            print("KEbJ is less than 0, set to 0")

    #Calculate output velocity
    def cal_Vb(self):
        self.Vb = math.sqrt((self.KEbJ / (0.5 * self.MFR)))

    #Calculate engine thrust
    def cal_thrust(self):
        self.thrust = self.MFR * (self.Vb - self.Va)
        if (self.thrust < 0):
            self.thrust = 0
            print("thrust is less than 0, set to 0")

    #Account for thrust losses in nozzle
    def cal_nozzle_thrust_coeff(self):
        self.thrust = self.thrust * (SettingsClass.settings.config_list[0] / 100)

    #Print turbine values in console
    def display_values(self):
        print("Temperatures:")
        print("Ta: ", self.Ta)
        print("T1: ", self.T1)
        print("T2s: ", self.T2s)
        print("T2a: ", self.T2a)
        print("T3: ", self.T3)
        print("T4s: ", self.T4s)
        print("T4a: ", self.T4a)
        print("Tb: ", self.Tb)

        print("Pressures:")
        print("Pa: ", self.Pa)
        print("P1: ", self.P1)
        print("P2: ", self.P2)
        print("P3: ", self.P3)
        print("P4: ", self.P4)
        print("Pb: ", self.Pb)

        print("Kinetic Energies:")
        print("KEaJ: ", self.KEaJ)
        print("KEbJ: ", self.KEbJ)

        print("Air Velocities:")
        print("Va: ", self.Va)
        print("Vb: ", self.Vb)

        print("Thrust: ", self.thrust)

    #Set turbine values
    #Set input velocity
    def set_Va(self, Va):
        self.Va = Va

    #Set mass flow rate
    def set_MFR(self, MFR):
        self.MFR = MFR

    #Set pressure ratio
    def set_CPR(self, CPR):
        self.CPR = CPR

    #Set compressor efficiency
    def set_NPC(self, NPC):
        self.NPC = NPC

    #Set turbine efficiency
    def set_NPT(self, NPT):
        self.NPT = NPT

    #Set ambient temperature
    def set_Ta(self, Ta):
        self.Ta = Ta

    #Set ambient pressure
    def set_Pa(self, Pa):
        self.Pa = Pa

    #Set ambient pressure
    def set_Pb(self, Pb):
        self.Pb = Pb

    #Set combustor output temperature
    def set_T3(self, T3):
        self.T3 = T3

    #Get turbine input values
    #Get input temperature
    def get_Ta(self):
        return self.Ta

    #Get input pressure
    def get_Pa(self):
        return self.Pa

    #Get output pressure
    def get_Pb(self):
        return self.Pb

    #Get input velocity
    def get_Va(self):
        return self.Va

    #Get mass flow rate
    def get_MFR(self):
        return self.MFR

    #Get compressor ratio
    def get_CPR(self):
        return self.CPR

    #Get compressor efficiency
    def get_NPC(self):
        return self.NPC

    #Get turbine efficiency
    def get_NPT(self):
        return self.NPT

    #Get turbine values
    #Get input kinetic energy (J)
    def get_KEaJ(self):
        return self.KEaJ

    #Get input kinetic energy (KJ/KG)
    def get_KEaKJKG(self):
        return self.KEaKJKG

    #Get ouput kinetic energy (J)
    def get_KEbJ(self):
        return self.KEbJ

    #Get ouput kinetic energy (KJ/KG)
    def get_KEbKJKG(self):
        return self.KEbKJKG

    #Get temperautre at 1
    def get_T1(self):
        return self.T1

    #Get temperautre at 2s
    def get_T2s(self):
        return self.T2s

    # Get temperautre at 2a
    def get_T2a(self):
        return self.T2a

    def get_T3(self):
        return self.T3

    #Get temperautre at 4s
    def get_T4s(self):
        return self.T4s

    #Get temperautre at 4a
    def get_T4a(self):
        return self.T4a

    #Get temperautre at output
    def get_Tb(self):
        return self.Tb

    #Get Pressure at 1
    def get_P1(self):
        return self.P1

    #Get Pressure at 2
    def get_P2(self):
        return self.P2

    #Get Pressure at 3
    def get_P3(self):
        return self.P3

    #Get Pressure at 4
    def get_P4(self):
        return self.P4

    #Get output velocity
    def get_Vb(self):
        return self.Vb

    #Get engine thrust
    def get_thrust(self):
        return self.thrust

    #Calculate engine values
    def tick_engine(self):
        if(self.MFR > 0):
            self.cal_KEaJ()
            self.conv_to_KEaKJKG()
            self.cal_T1()
            self.cal_P1()
            self.cal_P2()
            self.cal_P3()
            self.cal_T2s()
            self.cal_T2a()
            self.cal_T4a()
            self.cal_T4s()
            self.cal_P4()
            self.cal_jetpipe_pressure_loss()
            self.cal_Tb()
            self.cal_KEbKJKG()
            self.conv_to_KEbJ()
            self.cal_Vb()
            self.cal_thrust()
            self.cal_nozzle_thrust_coeff()
        else:
            self.reset_values()

    #Set engine values to 0 if engine off (0 rpm)
    def reset_values(self):
        # Kinetic Energy variables
        self.KEaJ = 0
        self.KEaKJKG = 0
        self.KEbJ = 0
        self.KEbKJKG = 0

        # Temperatures
        self.T1 = 0
        self.T2s = 0
        self.T2a = 0
        self.T4s = 0
        self.T4a = 0
        self.Tb = 0

        # Pressures
        self.P1 = 0
        self.P2 = 0
        self.P3 = 0
        self.P4 = 0

        # Air velocities
        self.Vb = 0

        # Engine Thrust
        self.thrust = 0

    #Collates engine data into list and sends to "SettingsClass"
    def send_data_to_log(self):
        data_list = []

        data_list.append(self.get_T1())
        data_list.append(self.get_T2s())
        data_list.append(self.get_T2a())
        data_list.append(self.get_T4s())
        data_list.append(self.get_T4a())

        data_list.append(self.get_P1())
        data_list.append(self.get_P2())
        data_list.append(self.get_P3())
        data_list.append(self.get_P4())

        data_list.append(self.get_KEaJ())
        data_list.append(self.get_KEbJ())

        data_list.append(self.get_Va())
        data_list.append(self.get_Vb())

        data_list.append(self.get_thrust())

        SettingsClass.settings.log_data(data_list)
