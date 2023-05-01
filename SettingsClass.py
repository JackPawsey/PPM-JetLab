#Imports
import os

#Initialises config settings and handles external files
class SettingsClass():
    def __init__(self):

        # nozzle_thrust_coeff, turbine_inlet_temp, combustor_pressure_loss, jetpipe_pressure_loss, intake_recovery_factor,
        # Ta, Pa, T3, K, Cp, graph1_refresh_rate, graph2_refresh_rate
        self.default_values = [99, 5, 1, 220, 26, 700, 1.385, 1.032, 1000, 1000]

        self.config_list = []

        try:
            self.load_config()
        except Exception as e:
            self.create_default_config()

    #Reads from an existing config file to populate the "config_list" list
    def load_config(self):
        config_file = open("config.txt", "r")

        num_lines = sum(1 for line in open("config.txt"))

        print("Config file found, loading...")

        self.config_list.clear()

        for x in range(num_lines):
            a_line = config_file.readline()

            try:
                self.config_list.append(int(a_line))
            except:
                self.config_list.append(float(a_line))

        config_file.close()

    #Writes the current "config_list" to an existing config file
    def save_config(self):
        config_file = open("config.txt", "w")

        print("Saving config to file...")

        for x in range(len(self.config_list)):
            config_file.write(str(self.config_list[x]) + '\n')

        config_file.close()

    #Creates a external .txt config and writes defualt values to it
    def create_default_config(self):
        print("Config file not found, creating default...")

        config_file = open("config.txt", "w+")

        for x in range(len(self.default_values)):
            config_file.write(str(self.default_values[x]) + '\n')

        config_file.close()

        self.load_config()

    #Output engine data to log
    def log_data(self, data_list):

        if (os.path.isfile("data_log.txt")):
            self.save_to_log(data_list)
        else:
            self.create_new_log(data_list)

    #Generate new data log and output engine data
    def create_new_log(self, data_list):
        print("No data log foud...creating new data log...")

        log_file = open("data_log.txt", "w")

        log_file.write("T1:  T2s: T2a: T4s: T4a: P1:  P2:  P3:  P4:  KEaJ:   KEbJ:   Va:  Vb:  Thrust:" + '\n')

        for x in range(len(data_list)):
            log_file.write(str(round(data_list[x])))
            log_file.write("  ")

        log_file.write('\n')

        log_file.close()

    #Output engine data to existing data log
    def save_to_log(self, data_list):
        print("Existing data log found...appending...")

        log_file = open("data_log.txt", "a")

        for x in range(len(data_list)):
            log_file.write(str(round(data_list[x])))
            log_file.write("  ")

        log_file.write('\n')

        log_file.close()

#Creates a global instance of "SettingsClass"
def init():
    global settings

    settings = SettingsClass()