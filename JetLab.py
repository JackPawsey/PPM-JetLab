#Imports
import tkinter as tk
from tkinter import filedialog
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import math
import os
import sys

#Import local classes
import TurbineClass as TC
import SettingsClass as SC
import TableClass

#Initialise global instance of "SettingsClass" as "settings"
SC.init()

#Set graph style
style.use("ggplot")

#Globals
#Fonts
LARGE_FONT = ("Courier New", 25)
MIDDLE_FONT = ("Courier New", 15)
SMALL_FONT = ("Courier New", 12)

#Create graph 1
graph1 = plt.figure(figsize=(7, 4), dpi=100)
graph1_ax = graph1.add_subplot(111)

#Create graph 2
graph2 = plt.figure(figsize=(7, 4), dpi=100)
graph2_ax = graph2.add_subplot(111)

#Create engine instance
turbine = TC.GasTurbine(200, 18, 8, 0.85, 0.90)

#Graph 1 plot value lists
graph1_x_list = []
graph1_y_list = []

#Graph 2 plot value lists
graph2_x_list = []
graph2_y_list = []

#Used to get value from rpm only when animate() is called
latest_value = 0

#Global variables used to determine when plot choice is changed
graph1_new_choice = 0
graph1_old_choice = 0

graph2_new_choice = 1
graph2_old_choice = 1

#Global variables used to store what units have been selected
temp_unit_choice = 0
pressure_unit_choice = 0
velocity_unit_choice = 0
KE_unit_choice = 0

#Create global variable used to hold path to working directory
base_folder = os.path.dirname(__file__)

#List of plottable values
plot_list = ["Input Kinetic Energy", "Temperature at 1", "Temperature at 2 (Isentropic)",
             "Temperature at 2 (Actual)", "Temperature at 4 (Isentropic)", "Temperautre at 4 (Actual)",
             "Exhuast Temperature", "Pressure at 1", "Pressure at 2", "Pressure at 3", "Pressure at 4",
             "Exhaust Velocity", "Output Kinetic Energy", "Thrust", "RPM"]

#Initialisation class that creates frames and menu
class Start(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Set window icon
        image_path = os.path.join(base_folder, 'images/fan_icon.ico')
        tk.Tk.wm_iconbitmap(self, default=image_path)

        #Set window title
        tk.Tk.wm_title(self, "JetLab")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Create menubar
        self.menu_bar = tk.Menu(container)

        #Add submenu for primary options
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load Settings", command=lambda: load_settings())
        file_menu.add_command(label="Save Settings", command=lambda: save_settings())
        file_menu.add_separator()
        file_menu.add_command(label="Preferences", command=lambda: preferences_popup())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=sys.exit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        #Add submenu to control graph refresh rate
        self.refresh_rate_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.refresh_rate_menu.add_command(label="Set Graph 1 Refresh Rate", command=lambda: set_refresh_popup(1))
        self.refresh_rate_menu.add_separator()
        self.refresh_rate_menu.add_command(label="Set Graph 2 Refresh Rate", command=lambda: set_refresh_popup(2))
        self.menu_bar.add_cascade(label="Graph Refresh Rates", menu=self.refresh_rate_menu)

        #Add submenu for graph 1
        self.graph1_units_menu = tk.Menu(self.menu_bar, tearoff=1)
        self.graph1_units_menu.add_command(label=plot_list[0], background="red",
                                           command=lambda:[set_plot_choice(1, 0), self.highlight_plot_choice(1, 0)])
        self.graph1_units_menu.add_command(label=plot_list[1],
                                           command=lambda:[set_plot_choice(1, 1), self.highlight_plot_choice(1, 1)])
        self.graph1_units_menu.add_command(label=plot_list[2],
                                           command=lambda:[set_plot_choice(1, 2), self.highlight_plot_choice(1, 2)])
        self.graph1_units_menu.add_command(label=plot_list[3],
                                           command=lambda:[set_plot_choice(1, 3), self.highlight_plot_choice(1, 3)])
        self.graph1_units_menu.add_command(label=plot_list[4],
                                           command=lambda:[set_plot_choice(1, 4), self.highlight_plot_choice(1, 4)])
        self.graph1_units_menu.add_command(label=plot_list[5],
                                           command=lambda:[set_plot_choice(1, 5), self.highlight_plot_choice(1, 5)])
        self.graph1_units_menu.add_command(label=plot_list[6],
                                           command=lambda:[set_plot_choice(1, 6), self.highlight_plot_choice(1, 6)])
        self.graph1_units_menu.add_command(label=plot_list[7],
                                           command=lambda:[set_plot_choice(1, 7), self.highlight_plot_choice(1, 7)])
        self.graph1_units_menu.add_command(label=plot_list[8],
                                           command=lambda:[set_plot_choice(1, 8), self.highlight_plot_choice(1, 8)])
        self.graph1_units_menu.add_command(label=plot_list[9],
                                           command=lambda:[set_plot_choice(1, 9), self.highlight_plot_choice(1, 9)])
        self.graph1_units_menu.add_command(label=plot_list[10],
                                           command=lambda:[set_plot_choice(1, 10), self.highlight_plot_choice(1, 10)])
        self.graph1_units_menu.add_command(label=plot_list[11],
                                           command=lambda:[set_plot_choice(1, 11), self.highlight_plot_choice(1, 11)])
        self.graph1_units_menu.add_command(label=plot_list[12],
                                           command=lambda:[set_plot_choice(1, 12), self.highlight_plot_choice(1, 12)])
        self.graph1_units_menu.add_command(label=plot_list[13],
                                           command=lambda:[set_plot_choice(1, 13), self.highlight_plot_choice(1, 13)])
        self.graph1_units_menu.add_command(label=plot_list[14],
                                           command=lambda: [set_plot_choice(1, 14), self.highlight_plot_choice(1, 14)])
        self.menu_bar.add_cascade(label="Select Graph 1 Data", menu=self.graph1_units_menu)

        #Add submenu for graph 2
        self.graph2_units_menu = tk.Menu(self.menu_bar, tearoff=1)
        self.graph2_units_menu.add_command(label=plot_list[0],
                                           command=lambda: [set_plot_choice(2, 0), self.highlight_plot_choice(2, 0)])
        self.graph2_units_menu.add_command(label=plot_list[1], background="red",
                                           command=lambda: [set_plot_choice(2, 1), self.highlight_plot_choice(2, 1)])
        self.graph2_units_menu.add_command(label=plot_list[2],
                                           command=lambda: [set_plot_choice(2, 2), self.highlight_plot_choice(2, 2)])
        self.graph2_units_menu.add_command(label=plot_list[3],
                                           command=lambda: [set_plot_choice(2, 3), self.highlight_plot_choice(2, 3)])
        self.graph2_units_menu.add_command(label=plot_list[4],
                                           command=lambda: [set_plot_choice(2, 4), self.highlight_plot_choice(2, 4)])
        self.graph2_units_menu.add_command(label=plot_list[5],
                                           command=lambda: [set_plot_choice(2, 5), self.highlight_plot_choice(2, 5)])
        self.graph2_units_menu.add_command(label=plot_list[6],
                                           command=lambda: [set_plot_choice(2, 6), self.highlight_plot_choice(2, 6)])
        self.graph2_units_menu.add_command(label=plot_list[7],
                                           command=lambda: [set_plot_choice(2, 7), self.highlight_plot_choice(2, 7)])
        self.graph2_units_menu.add_command(label=plot_list[8],
                                           command=lambda: [set_plot_choice(2, 8), self.highlight_plot_choice(2, 8)])
        self.graph2_units_menu.add_command(label=plot_list[9],
                                           command=lambda: [set_plot_choice(2, 9), self.highlight_plot_choice(2, 9)])
        self.graph2_units_menu.add_command(label=plot_list[10],
                                           command=lambda: [set_plot_choice(2, 10), self.highlight_plot_choice(2, 10)])
        self.graph2_units_menu.add_command(label=plot_list[11],
                                           command=lambda: [set_plot_choice(2, 11), self.highlight_plot_choice(2, 11)])
        self.graph2_units_menu.add_command(label=plot_list[12],
                                           command=lambda: [set_plot_choice(2, 12), self.highlight_plot_choice(2, 12)])
        self.graph2_units_menu.add_command(label=plot_list[13],
                                           command=lambda: [set_plot_choice(2, 13), self.highlight_plot_choice(2, 13)])
        self.graph2_units_menu.add_command(label=plot_list[14],
                                           command=lambda: [set_plot_choice(2, 14), self.highlight_plot_choice(1, 14)])
        self.menu_bar.add_cascade(label="Select Graph 2 Data", menu=self.graph2_units_menu)

        #Add submenu to change units
        units_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Change Units", menu=units_menu)
        self.KE_submenu = tk.Menu(units_menu, tearoff=0)
        self.KE_submenu.add_command(label="Joules (J)", background="red", command=lambda: [set_unit_choice(0, 0), self.highlight_unit_choice(0, 0)])
        self.KE_submenu.add_command(label="Kilojoules Per Kilogram (KJ/KG)", command=lambda: [set_unit_choice(1, 0), self.highlight_unit_choice(0, 1)])
        units_menu.add_cascade(label="Kinetic Energy Units", menu=self.KE_submenu)
        self.temp_submenu = tk.Menu(units_menu, tearoff=0)
        self.temp_submenu.add_command(label="Degrees Celcius (C)", command=lambda: [set_unit_choice(2, 1), self.highlight_unit_choice(1, 0)])
        self.temp_submenu.add_command(label="Degrees Farenheit (F)", command=lambda: [set_unit_choice(1, 1), self.highlight_unit_choice(1, 1)])
        self.temp_submenu.add_command(label="Kelvin (K)", background="red", command=lambda: [set_unit_choice(0, 1), self.highlight_unit_choice(1, 2)])
        units_menu.add_cascade(label="Temperature Units", menu=self.temp_submenu)
        self.pressure_submenu = tk.Menu(units_menu, tearoff=0)
        self.pressure_submenu.add_command(label="Kilopascals (KPa)", background="red", command=lambda: [set_unit_choice(0, 2), self.highlight_unit_choice(2, 0)])
        self.pressure_submenu.add_command(label="Pounds Per Square Inch (PSI)", command=lambda: [set_unit_choice(1, 2), self.highlight_unit_choice(2, 1)])
        self.pressure_submenu.add_command(label="Atmospheres (Bar)", command=lambda: [set_unit_choice(2, 2), self.highlight_unit_choice(2, 2)])
        units_menu.add_cascade(label="Pressure Units", menu=self.pressure_submenu)
        self.velocity_submenu = tk.Menu(units_menu, tearoff=0)
        self.velocity_submenu.add_command(label="Meters Per Second (m/s)", background="red", command=lambda: [set_unit_choice(0, 3), self.highlight_unit_choice(3, 0)])
        self.velocity_submenu.add_command(label="Miles Per Hour (MPH)", command=lambda: [set_unit_choice(1, 3), self.highlight_unit_choice(3, 1)])
        self.velocity_submenu.add_command(label="Kilometers Per Hour (KPH)", command=lambda: [set_unit_choice(2, 3), self.highlight_unit_choice(3, 2)])
        units_menu.add_cascade(label="Velocity Units", menu=self.velocity_submenu)

        #Create frames/pages using page classes
        self.frames = {}
        for f in (MainScreen, StartScreen, HelpScreen, InputScreen):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Call local show frame method to display the first page
        self.show_frame(StartScreen)

    #Get a reference to another screen class from controller
    def get_page(self, page_class):
        return self.frames[page_class]

    #Set the page title
    def set_title(self, title):
        tk.Tk.wm_title(self, title)

    #Display the menubar
    def show_menu(self):
        tk.Tk.config(self, menu=self.menu_bar)

    #Switches between screens
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

    #Highlight the selected plot choice
    def highlight_plot_choice(self, graph, choice):
        for x in range(0, (len(plot_list) + 1)):
            if graph == 1:
                if (x == (choice + 1)):
                    self.graph1_units_menu.entryconfig(x, background="red")
                else:
                    self.graph1_units_menu.entryconfig(x, background="SystemButtonFace")
            else:
                if (x == (choice + 1)):
                    self.graph2_units_menu.entryconfig(x, background="red")
                else:
                    self.graph2_units_menu.entryconfig(x, background="SystemButtonFace")

    #Highlight the select unit choice
    def highlight_unit_choice(self, unit, choice):
        if unit == 0:
            for x in range(0, 2):
                if (x == choice):
                    self.KE_submenu.entryconfig(x, background="red")
                else:
                    self.KE_submenu.entryconfig(x, background="SystemButtonFace")
        elif unit == 1:
            for x in range(0, 3):
                if (x == choice):
                    self.temp_submenu.entryconfig(x, background="red")
                else:
                    self.temp_submenu.entryconfig(x, background="SystemButtonFace")
        elif unit == 2:
            for x in range(0, 3):
                if (x == choice):
                    self.pressure_submenu.entryconfig(x, background="red")
                else:
                    self.pressure_submenu.entryconfig(x, background="SystemButtonFace")
        else:
            for x in range(0, 3):
                if (x == choice):
                    self.velocity_submenu.entryconfig(x, background="red")
                else:
                    self.velocity_submenu.entryconfig(x, background="SystemButtonFace")


# Start page
class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Create local reference to controller (StartClass)
        self.controller = controller

        #Create image and place it in label for background
        login_image_path = os.path.join(base_folder, 'images/login_page_image.png')
        turbine_image = tk.PhotoImage(file=login_image_path, master=self)
        turbine_image_l = tk.Label(self, image=turbine_image)
        turbine_image_l.image = turbine_image
        turbine_image_l.place(x=-2, y=-3)

        start_b = tk.Button(self, text="Start", bg="#20a6cb", font=LARGE_FONT, relief='flat',
                             activebackground="#20a6cb", command=lambda: controller.show_frame(InputScreen))
        start_b.config(overrelief="raised", height=2, width=10)
        start_b.place(x=770, y=500)


#Input page
class InputScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Create local reference to controller (StartClass)
        self.controller = controller

        #Bind function to event, when 'ShowFrame' is called 'on_show_frame' is also
        self.bind("<<ShowFrame>>", self.on_show_frame)

        #Create image and place it in label for background
        login_image_path = os.path.join(base_folder, 'images/main_page_image.png')
        turbine_image = tk.PhotoImage(file=login_image_path, master=self)
        turbine_image_l = tk.Label(self, image=turbine_image)
        turbine_image_l.image = turbine_image
        turbine_image_l.place(x=-2, y=-3)

        #Label widgets
        max_rpm_l = tk.Label(self, text="Max RPM:", font=LARGE_FONT)
        mass_air_flow_l = tk.Label(self, text="Mass air flow (KG/s):", font=LARGE_FONT)
        pressure_ratio_l = tk.Label(self, text="Pressure Ratio:", font=LARGE_FONT)
        intake_velocity_l = tk.Label(self, text="Intake Velocity (m/s):", font=LARGE_FONT)
        max_rpm_info_l = tk.Label(self, text="Maximum speed the turbine's rotor can rotate: rotations per minute.", font=MIDDLE_FONT)
        mass_air_flow_info_l = tk.Label(self, text="Amount of air entering the turbine every second.", font=MIDDLE_FONT)
        pressure_ratio_info_l = tk.Label(self, text="Difference in pressure before and after the compressor.", font=MIDDLE_FONT)
        intake_velocity_info_l = tk.Label(self, text="Speed of air entering turbine, zero if stationary.", font=MIDDLE_FONT)

        #Entry widgets
        self.max_rpm_e = tk.Entry(self, width=10, font=LARGE_FONT)
        self.max_rpm_e.insert(0, 7000)
        self.max_mass_air_flow_e = tk.Entry(self, width=10, font=LARGE_FONT)
        self.max_mass_air_flow_e.insert(0, 20)
        self.pressure_ratio_e = tk.Entry(self, width=10, font=LARGE_FONT)
        self.pressure_ratio_e.insert(0, 10)
        self.intake_velocity_e = tk.Entry(self, width=10, font=LARGE_FONT)
        self.intake_velocity_e.insert(0, 200)

        #Button widgets
        self.reset_values_b = tk.Button(self, text="Reset to Default", bg="#20a6cb", font=LARGE_FONT, relief='flat',
                                        activebackground="#20a6cb", command=self.reset_input_default_values)
        self.reset_values_b.config(overrelief="raised")

        main_page_b = tk.Button(self, text="Main Page ->", bg="#20a6cb", font=MIDDLE_FONT, relief='flat',
                           activebackground="#20a6cb", command=self.validate_input_values)
        main_page_b.config(overrelief="raised")

        #Place widgets onto page
        max_rpm_l.place(x=25, y=300)
        mass_air_flow_l.place(x=25, y=350)
        pressure_ratio_l.place(x=25, y=400)
        intake_velocity_l.place(x=25, y=450)
        max_rpm_info_l.place(x=700, y=300)
        mass_air_flow_info_l.place(x=700, y=350)
        pressure_ratio_info_l.place(x=700, y=400)
        intake_velocity_info_l.place(x=700, y=450)

        self.max_rpm_e.place(x=470, y=300)
        self.max_mass_air_flow_e.place(x=470, y=350)
        self.pressure_ratio_e.place(x=470, y=400)
        self.intake_velocity_e.place(x=470, y=450)

        self.reset_values_b.place(x=25, y=600)
        main_page_b.place(x=1740, y=10)

    #Method ran when page is displayed
    def on_show_frame(self, event):
        self.controller.show_menu()
        self.controller.set_title("JetLab - Input Page")
        ani1.event_source.stop()
        ani2.event_source.stop()

    #Clear entries and enter default values
    def reset_input_default_values(self):
        self.max_rpm_e.delete(0, "end")
        self.max_mass_air_flow_e.delete(0, "end")
        self.pressure_ratio_e.delete(0, "end")
        self.intake_velocity_e.delete(0, "end")

        self.max_rpm_e.insert(0, 7000)
        self.max_mass_air_flow_e.insert(0, 20)
        self.pressure_ratio_e.insert(0, 10)
        self.intake_velocity_e.insert(0, 200)

    #Get the value from max rpm entry
    def get_max_rpm_e(self):
        return self.max_rpm_e.get()

    #Get the value from max mass air flow entry
    def get_max_mass_air_flow_e(self):
        return self.max_mass_air_flow_e.get()

    #Get the value from pressure ratio entry
    def get_pressure_ratio_e(self):
        return self.pressure_ratio_e.get()

    #Get the value from intake velocity entry
    def get_intake_velocity_e(self):
        return self.intake_velocity_e.get()

    #Validate input values
    def validate_input_values(self):
        if (validate_int_input(self.get_max_rpm_e(), 100, 100000) and
                validate_int_input(self.get_max_mass_air_flow_e(), 1, 1000) and
                validate_int_input(self.get_pressure_ratio_e(), 1, 100) and
                validate_int_input(self.get_intake_velocity_e(), 0, 10000)):

            self.controller.show_frame(MainScreen)


# Main page
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Create local reference to controller (StartClass)
        self.controller = controller

        #Bind function to event, when 'ShowFrame' is called 'on_show_frame' is also
        self.bind("<<ShowFrame>>", self.on_show_frame)

        #Create image and place it in label for background
        main_image_path = os.path.join(base_folder, 'images/main_page_image.png')
        turbine_image = tk.PhotoImage(file=main_image_path, master=self)
        turbine_image_l = tk.Label(self, image=turbine_image)
        turbine_image_l.image = turbine_image
        turbine_image_l.place(x=-2, y=-3)

        # Create image and place it in label for background
        turbojet_diagram_path = os.path.join(base_folder, 'images/turbojet_diagram.png')
        turbojet_diagram = tk.PhotoImage(file=turbojet_diagram_path, master=self)
        turbojet_diagram_l = tk.Label(self, image=turbojet_diagram)
        turbojet_diagram_l.image = turbojet_diagram
        turbojet_diagram_l.place(x=500, y=530)

        self.comp_eff = tk.DoubleVar(self)
        self.turbine_eff = tk.DoubleVar(self)
        self.max_rpm = tk.DoubleVar(self)
        self.throttle_value = tk.DoubleVar(self)
        self.pressure_ratio = tk.DoubleVar(self)
        self.intake_velocity = tk.DoubleVar(self)
        self.max_mass_air_flow = tk.DoubleVar(self)
        self.curr_mass_air_flow = tk.DoubleVar(self)
        self.current_rpm = tk.DoubleVar(self)
        self.thrust = tk.DoubleVar(self)
        self.comp_eff.set(85)
        self.turbine_eff.set(85)
        self.max_rpm.set(7000)
        self.throttle_value.set(0.0)
        self.pressure_ratio.set(0.0)
        self.intake_velocity.set(0.0)
        self.max_mass_air_flow.set(20)
        self.curr_mass_air_flow.set(0.0)
        self.current_rpm.set(0.0)
        self.sim_running = False

        #Lists to hold values for tables
        self.value_list1 = []
        self.value_list2 = []

        #Label widgets
        comp_eff_slider_l = tk.Label(self, text="Compressor Efficiency (%):", wraplength=120, font=SMALL_FONT)
        turbine_eff_slider_l = tk.Label(self, text="Turbine Efficiency (%):", wraplength=120, font=SMALL_FONT)
        throttle_control_slider_l = tk.Label(self, text="Throttle control (%):", wraplength=100, font=SMALL_FONT)
        comp_eff_out_l = tk.Label(self, textvariable=self.comp_eff, font=LARGE_FONT, foreground="green")
        turbine_eff_out_l = tk.Label(self, textvariable=self.turbine_eff, font=LARGE_FONT, foreground="green")
        rpm_out_l = tk.Label(self, textvariable=self.current_rpm, font=LARGE_FONT, foreground="green")
        rpm_l = tk.Label(self, text="RPM:", font=MIDDLE_FONT)
        comp_eff_l = tk.Label(self, text="Compressor Efficiency (%):", font=MIDDLE_FONT, wraplength=200)
        turbine_eff_l = tk.Label(self, text="Turbine Efficiency (%):", font=MIDDLE_FONT, wraplength=200)
        thrust_out_l = tk.Label(self, textvariable=self.thrust, font=LARGE_FONT, foreground="green")
        thrust_l = tk.Label(self, text="Thrust (N):", font=MIDDLE_FONT, wraplength=200)

        #Button widgets
        self.start_sim_b = tk.Button(self, text="Start Simulation", font=LARGE_FONT, relief='flat',
                                     activebackground="#20a6cb", command=self.toggle_simulation)
        self.start_sim_b.config(overrelief="raised", bg="red")
        help_page_b = tk.Button(self, text="Help Page ->", bg="#20a6cb", font=MIDDLE_FONT, relief='flat',
                                        activebackground="#20a6cb", command=lambda: controller.show_frame(HelpScreen))
        help_page_b.config(overrelief="raised")
        input_page_b = tk.Button(self, text="<- Input Page", bg="#20a6cb", font=MIDDLE_FONT, relief='flat',
                           activebackground="#20a6cb", command=lambda: controller.show_frame(InputScreen))
        input_page_b.config(overrelief="raised")

        #Slider widgets
        self.comp_eff_s = tk.Scale(self, orient="vertical", length=400, width=60, sliderlength=30, from_=100, to=1,
                                   tickinterval=25, variable=self.comp_eff, background="#20a6cb",
                                   activebackground="grey", font=SMALL_FONT, borderwidth=0, foreground="white",
                                   troughcolor="#8c8c8c", command=self.update_values)
        self.turbine_eff_s = tk.Scale(self, orient="vertical", length=400, width=60, sliderlength=30, from_=100, to=1,
                                      tickinterval=25, variable=self.turbine_eff, background="#20a6cb",
                                      activebackground="grey", font=SMALL_FONT, borderwidth=0, foreground="white",
                                      troughcolor="#8c8c8c", command=self.update_values)
        self.throttle_s = tk.Scale(self, orient="vertical", length=400, width=60, sliderlength=30, from_=100, to=0,
                                   tickinterval=25, variable=self.throttle_value, command=self.update_values,
                                   background="#20a6cb", activebackground="grey", font=SMALL_FONT, borderwidth=0,
                                   foreground="white", troughcolor="#8c8c8c")

        #Place widgets onto page
        throttle_control_slider_l.place(x=25, y=470)
        comp_eff_slider_l.place(x=160, y=470)
        turbine_eff_slider_l.place(x=295, y=470)
        rpm_out_l.place(x=230, y=250)
        comp_eff_out_l.place(x=230, y=300)
        turbine_eff_out_l.place(x=230, y=350)
        rpm_l.place(x=25, y=250)
        comp_eff_l.place(x=25, y=300)
        turbine_eff_l.place(x=25, y=350)
        thrust_out_l.place(x=230, y=400)
        thrust_l.place(x=25, y=400)

        self.start_sim_b.place(x=250, y=10)
        help_page_b.place(x=1740, y=10)
        input_page_b.place(x=15, y=10)
        self.throttle_s.place(x=25, y=530)
        self.comp_eff_s.place(x=160, y=530)
        self.turbine_eff_s.place(x=295, y=530)

        #Create graph 1
        graph1_canvas = FigureCanvasTkAgg(graph1, self)
        graph1_canvas.draw()
        graph1_canvas.get_tk_widget().place(x=1200, y=60)

        #Create graph 1 toolbar
        graph1_toolbar = NavigationToolbar2Tk(graph1_canvas, self)
        graph1_toolbar.update()
        graph1_toolbar.place(x=1200, y=460)

        #Create graph 2
        graph2_canvas = FigureCanvasTkAgg(graph2, self)
        graph2_canvas.draw()
        graph2_canvas.get_tk_widget().place(x=1200, y=530)

        #Create graph 2 toolbar
        graph2_toolbar = NavigationToolbar2Tk(graph2_canvas, self)
        graph2_toolbar.update()
        graph2_toolbar.place(x=1200, y=930)

        #Create temperature & pressure table
        self.value_table1 = TableClass.Table(self, 3, 9)
        self.value_table1.place(x=750, y=160)

        #Set static table values
        self.value_table1.set(0, 0, "Stage:")
        self.value_table1.set(1, 0, "Temperature (K):")
        self.value_table1.set(2, 0, "Pressure (KPa):")
        self.value_table1.set(0, 1, "A:")
        self.value_table1.set(0, 2, "1:")
        self.value_table1.set(0, 3, "2s:")
        self.value_table1.set(0, 4, "2a:")
        self.value_table1.set(0, 5, "3:")
        self.value_table1.set(0, 6, "4s:")
        self.value_table1.set(0, 7, "4a:")
        self.value_table1.set(0, 8, "B:")

        #Create kinetic energy & velocity table
        self.value_table2 = TableClass.Table(self, 3, 3)
        self.value_table2.place(x=750, y=350)

        #Set static table values
        self.value_table2.set(0, 0, "Stage:")
        self.value_table2.set(1, 0, "Kinetic Energy (J):")
        self.value_table2.set(2, 0, "Velocity (m/s):")
        self.value_table2.set(0, 1, "A:")
        self.value_table2.set(0, 2, "B:")

    #Function ran when page is displayed
    def on_show_frame(self, event):
        self.input_screen = self.controller.get_page(InputScreen)
        self.controller.set_title("JetLab - Main Page")
        self.update_page()

    #Update graphical aspects of main page
    def update_page(self):
        self.update_table1()
        self.update_table2()

        #Update thrust value
        self.thrust.set(round(turbine.get_thrust()))

    #Add data from turbine to temperature & pressure table
    def update_table1(self):
        self.value_list1.clear()
        self.value_list1.append([round(turbine.get_Ta(), 1), round(turbine.get_T1(), 1), round(turbine.get_T2s(), 1),
                                round(turbine.get_T2a(), 1), round(turbine.get_T3(), 1), round(turbine.get_T4s(), 1),
                                round(turbine.get_T4a(), 1), round(turbine.get_Tb(), 1)])
        self.value_list1.append([round(turbine.get_Pa(), 1), round(turbine.get_P1(), 1), round(turbine.get_P2(), 1),
                                round(turbine.get_P2(), 1), round(turbine.get_P3(), 1), round(turbine.get_P4(), 1),
                                round(turbine.get_P4(), 1), round(turbine.get_Pb(), 1)])

        for x in range(1, 3):
            for y in range(1, 9):
                self.value_table1.set(x, y, self.value_list1[x - 1][y - 1])

    #Add data from turbine to kinetic energy & velocity table
    def update_table2(self):
        self.value_list2.clear()
        self.value_list2.append([round(turbine.get_KEaJ(), 1), round(turbine.get_KEbJ(), 1)])
        self.value_list2.append([round(turbine.get_Va(), 1), round(turbine.get_Vb(), 1)])

        for x in range(1, 3):
            for y in range(1, 3):
                self.value_table2.set(x, y, self.value_list2[x - 1][y - 1])

    #Jumper function used to call two functions when throttle slider is moved
    def update_values(self, *args):
        self.calculate_rpm()
        self.calculate_mfr()

        if (self.sim_running):
            self.run_simulation()

    #Get current throttle position and use to calculate engine rpm
    def calculate_rpm(self):
        global latest_value

        self.current_rpm.set(round((self.throttle_value.get() / 100) * self.max_rpm.get()))
        latest_value = int(self.current_rpm.get())

    #Get current throttle position and use to calculate mfr
    def calculate_mfr(self):
        self.curr_mass_air_flow.set((float(self.input_screen.get_max_mass_air_flow_e()) / 100) * self.throttle_value.get())

    #Toggle simulation on and off
    def toggle_simulation(self):
        if not self.sim_running:
            self.start_sim_b.config(overrelief="raised", bg="green", text="Stop Simulation")
            self.sim_running = True
            control_graph_ani(1, True)
            control_graph_ani(2, True)
            print("Simulation running...")
        elif self.sim_running:
            self.start_sim_b.config(overrelief="raised", bg="red", text="Start Simulation")
            self.sim_running = False
            control_graph_ani(1, False)
            control_graph_ani(2, False)
            print("Simulation off...")

    #Input values into turbine instance, perform calculations, save new values to data log, update labels
    def run_simulation(self):
        turbine.set_Va(float(self.input_screen.get_intake_velocity_e()))
        turbine.set_MFR(float(self.curr_mass_air_flow.get()))
        turbine.set_CPR(float(self.input_screen.get_pressure_ratio_e()))
        turbine.set_NPC(self.comp_eff_s.get())
        turbine.set_NPT(self.turbine_eff.get())

        turbine.tick_engine()
        print("engine tick...")
        turbine.send_data_to_log()

        self.update_page()


#Help page
class HelpScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Create local reference to controller (StartClass)
        self.controller = controller

        #Bind function to event, when 'ShowFrame' is called 'on_show_frame' is also
        self.bind("<<ShowFrame>>", self.on_show_frame)

        #Create image and place it in label for background
        login_image_path = os.path.join(base_folder, 'images/main_page_image.png')
        turbine_image = tk.PhotoImage(file=login_image_path, master=self)
        turbine_image_l = tk.Label(self, image=turbine_image)
        turbine_image_l.image = turbine_image
        turbine_image_l.place(x=-2, y=-3)

        #Create image and place it in label for background
        help_diagram_image_path = os.path.join(base_folder, 'images/help_diagram.png')
        help_diagram = tk.PhotoImage(file=help_diagram_image_path, master=self)
        help_diagram_l = tk.Label(self, image=help_diagram)
        help_diagram_l.image = help_diagram
        help_diagram_l.place(x=520, y=580)

        #Label widgets
        stage_A_l = tk.Label(self, text="A: Ta, Pa, Va, KEa", font=MIDDLE_FONT)
        stage_1_l = tk.Label(self, text="1: T1, P1", font=MIDDLE_FONT)
        stage_2_l = tk.Label(self, text="2: T2s/T2a, P2", font=MIDDLE_FONT)
        stage_3_l = tk.Label(self, text="3: T3, P3", font=MIDDLE_FONT)
        stage_4_l = tk.Label(self, text="4: T4s/T4a, P4", font=MIDDLE_FONT)
        stage_b_l = tk.Label(self, text="B: Tb, Pb, KEb", font=MIDDLE_FONT)

        #Button widgets
        main_page_b = tk.Button(self, text="<- Main Page", bg="#20a6cb", font=MIDDLE_FONT, relief='flat',
                             activebackground="#20a6cb", command=lambda: controller.show_frame(MainScreen))
        main_page_b.config(overrelief="raised")

        #Text widgets
        instruction_text ="""Operation Instructions:
•Provide values on 'Input Page' to determine physical/enviromental 
 factors that will effect the turbine
•Press 'Run Simulation' and move sliders to adjust turbine operating 
 parameters
•Data plotted onto graphs and its respective units can be specified 
 using the menubar
•Frequency of graph updates can be entered using menubar->'Graph 
 Refresh Rates'
•Advanced options can be seen in menubar->File->Preferences"""

        about_text ="""About:
This program allow the real-time visualisation of gas turbine data 
through the use of graphs and sliders.

Assumptions/Factors unaccounted for:
    •No afterburner
    •Sea level altitude operation
    •Generic unspecified fuel
    •Startup/shutdown procedures
    •Number/performance of compressor/turbine stages"""

        instruction_text_t = tk.Text(self, height=10, width=73, padx=10, pady=5, spacing1=10, font=MIDDLE_FONT,
                                   borderwidth=0)
        instruction_text_t.insert(tk.END, instruction_text)
        instruction_text_t.config(state="disabled")

        about_text_t = tk.Text(self, height=10, width=78, padx=10, pady=5, spacing1=10, font=MIDDLE_FONT,
                                   borderwidth=0)
        about_text_t.insert(tk.END, about_text)
        about_text_t.config(state="disabled")

        #Place widgets onto page
        stage_A_l.place(x=520, y=580)
        stage_1_l.place(x=670, y=905)
        stage_2_l.place(x=800, y=580)
        stage_3_l.place(x=950, y=905)
        stage_4_l.place(x=1050, y=580)
        stage_b_l.place(x=1220, y=905)

        main_page_b.place(x=15, y=10)

        instruction_text_t.place(x=25, y=140)
        about_text_t.place(x=940, y=140)

    #Function ran when page is displayed
    def on_show_frame(self, event):
        self.controller.set_title("JetLab - Help Page")


#Animation function for graph 1
def animate_graph1(i):
    global graph1_new_choice, graph1_old_choice

    #Append turbine data to list depending on plot choice and unit choice, set graph label
    def choose_plot(plot_choice):
        if plot_choice == 0 and KE_unit_choice == 0:
            graph1_y_list.append(turbine.get_KEaJ())
            graph1_ax.set_ylabel("Joules (J)")
            plot_data(plot_choice)
        elif plot_choice == 0 and KE_unit_choice == 1:
            graph1_y_list.append(turbine.get_KEaKJKG())
            graph1_ax.set_ylabel("Kilojoules Per Kilogram (KJ/KG)")
            plot_data(plot_choice)

        elif plot_choice == 1 and temp_unit_choice == 2:
            graph1_y_list.append(kelvin_to_celsius(turbine.get_T1()))
            graph1_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 1 and temp_unit_choice == 1:
            graph1_y_list.append(kelvin_to_farenheit(turbine.get_T1()))
            graph1_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 1 and temp_unit_choice == 0:
            graph1_y_list.append(turbine.get_T1())
            graph1_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 2 and temp_unit_choice == 2:
            graph1_y_list.append(kelvin_to_celsius(turbine.get_T2s()))
            graph1_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 2 and temp_unit_choice == 1:
            graph1_y_list.append(kelvin_to_farenheit(turbine.get_T2s()))
            graph1_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 2 and temp_unit_choice == 0:
            graph1_y_list.append(turbine.get_T2s())
            graph1_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 3 and temp_unit_choice == 2:
            graph1_y_list.append(kelvin_to_celsius(turbine.get_T2a()))
            graph1_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 3 and temp_unit_choice == 1:
            graph1_y_list.append(kelvin_to_farenheit(turbine.get_T2a()))
            graph1_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 3 and temp_unit_choice == 0:
            graph1_y_list.append(turbine.get_T2a())
            graph1_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 4 and temp_unit_choice == 2:
            graph1_y_list.append(kelvin_to_celsius(turbine.get_T4a()))
            graph1_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 4 and temp_unit_choice == 1:
            graph1_y_list.append(kelvin_to_farenheit(turbine.get_T4a()))
            graph1_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 4 and temp_unit_choice == 0:
            graph1_y_list.append(turbine.get_T4a())
            graph1_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 5 and temp_unit_choice == 2:
            graph1_y_list.append(kelvin_to_celsius(turbine.get_T4s()))
            graph1_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 5 and temp_unit_choice == 1:
            graph1_y_list.append(kelvin_to_farenheit(turbine.get_T4s()))
            graph1_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 5 and temp_unit_choice == 0:
            graph1_y_list.append(turbine.get_T4s())
            graph1_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 6 and temp_unit_choice == 2:
            graph1_y_list.append(kelvin_to_celsius(turbine.get_Tb()))
            graph1_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 6 and temp_unit_choice == 1:
            graph1_y_list.append(kelvin_to_farenheit(turbine.get_Tb()))
            graph1_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 6 and temp_unit_choice == 0:
            graph1_y_list.append(turbine.get_Tb())
            graph1_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 7 and pressure_unit_choice == 0:
            graph1_y_list.append(turbine.get_P1())
            graph1_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 7 and pressure_unit_choice == 2:
            graph1_y_list.append(kpa_to_psi(turbine.get_P1()))
            graph1_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 7 and pressure_unit_choice == 3:
            graph1_y_list.append(kpa_to_bar(turbine.get_P1()))
            graph1_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 8 and pressure_unit_choice == 0:
            graph1_y_list.append(turbine.get_P2())
            graph1_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 8 and pressure_unit_choice == 1:
            graph1_y_list.append(kpa_to_psi(turbine.get_P2()))
            graph1_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 8 and pressure_unit_choice == 2:
            graph1_y_list.append(kpa_to_bar(turbine.get_P2()))
            graph1_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 9 and pressure_unit_choice == 0:
            graph1_y_list.append(turbine.get_P3())
            graph1_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 9 and pressure_unit_choice == 1:
            graph1_y_list.append(kpa_to_psi(turbine.get_P3()))
            graph1_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 9 and pressure_unit_choice == 2:
            graph1_y_list.append(kpa_to_bar(turbine.get_P3()))
            graph1_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 10 and pressure_unit_choice == 0:
            graph1_y_list.append(turbine.get_P4())
            graph1_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 10 and pressure_unit_choice == 1:
            graph1_y_list.append(kpa_to_psi(turbine.get_P4()))
            graph1_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 10 and pressure_unit_choice == 2:
            graph1_y_list.append(kpa_to_bar(turbine.get_P4()))
            graph1_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 11 and velocity_unit_choice == 0:
            graph1_y_list.append(turbine.get_Vb())
            graph1_ax.set_ylabel("Meters Per Second (m/s)")
            plot_data(plot_choice)
        elif plot_choice == 11 and velocity_unit_choice == 1:
            graph1_y_list.append(ms_to_mph(turbine.get_Vb()))
            graph1_ax.set_ylabel("Miles Per Hour (MPH)")
            plot_data(plot_choice)
        elif plot_choice == 11 and velocity_unit_choice == 2:
            graph1_y_list.append(ms_to_kph(turbine.get_Vb()))
            graph1_ax.set_ylabel("Kilometers Per Hour (KPH)")
            plot_data(plot_choice)

        elif plot_choice == 12 and KE_unit_choice == 0:
            graph1_y_list.append(turbine.get_KEbJ())
            graph1_ax.set_ylabel("Joules (J)")
            plot_data(plot_choice)
        elif plot_choice == 12 and KE_unit_choice == 1:
            graph1_y_list.append(turbine.get_KEbKJKG())
            graph1_ax.set_ylabel("Kilojoules Per Kilogram (KJ/KG)")
            plot_data(plot_choice)

        elif plot_choice == 13:
            graph1_y_list.append(turbine.get_thrust())
            graph1_ax.set_ylabel("Thrust (N)")
            plot_data(plot_choice)

        elif plot_choice == 14:
            graph1_y_list.append(latest_value)
            graph1_ax.set_ylabel("RPM")
            plot_data(plot_choice)

    #Plot data to graph
    def plot_data(plot_choice):
        graph1_x_list.append(i)
        graph1_ax.plot(graph1_x_list, graph1_y_list, color='b', label=plot_list[plot_choice])
        graph1_ax.legend()
        graph1_ax.set_title("Graph 1: " + plot_list[plot_choice] + " over Time")
        graph1_ax.set_xlabel("Time (s)")

    ani1.event_source.interval = SC.settings.config_list[8]

    graph1_ax.set_xlim(left=max(0, i - 50), right=i + 50)

    graph1_ax.clear()

    if graph1_old_choice == graph1_new_choice:
        choose_plot(graph1_new_choice)
    else:
        graph1_x_list.clear()
        graph1_y_list.clear()

        graph1_old_choice = graph1_new_choice

        choose_plot(graph1_new_choice)

#Animation function for graph 2
def animate_graph2(i):
    global graph2_new_choice, graph2_old_choice

    #Append turbine data to list depending on plot choice and unit choice, set graph label
    def choose_plot(plot_choice):
        if plot_choice == 0 and KE_unit_choice == 0:
            graph2_y_list.append(turbine.get_KEaJ())
            graph2_ax.set_ylabel("Joules (J)")
            plot_data(plot_choice)
        elif plot_choice == 0 and KE_unit_choice == 1:
            graph2_y_list.append(turbine.get_KEaKJKG())
            graph2_ax.set_ylabel("Kilojoules Per Kilogram (KJ/KG)")
            plot_data(plot_choice)

        elif plot_choice == 1 and temp_unit_choice == 2:
            graph2_y_list.append(kelvin_to_celsius(turbine.get_T1()))
            graph2_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 1 and temp_unit_choice == 1:
            graph2_y_list.append(kelvin_to_farenheit(turbine.get_T1()))
            graph2_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 1 and temp_unit_choice == 0:
            graph2_y_list.append(turbine.get_T1())
            graph2_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 2 and temp_unit_choice == 2:
            graph2_y_list.append(kelvin_to_celsius(turbine.get_T2s()))
            graph2_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 2 and temp_unit_choice == 1:
            graph2_y_list.append(kelvin_to_farenheit(turbine.get_T2s()))
            graph2_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 2 and temp_unit_choice == 0:
            graph2_y_list.append(turbine.get_T2s())
            graph2_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 3 and temp_unit_choice == 2:
            graph2_y_list.append(kelvin_to_celsius(turbine.get_T2a()))
            graph2_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 3 and temp_unit_choice == 1:
            graph2_y_list.append(kelvin_to_farenheit(turbine.get_T2a()))
            graph2_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 3 and temp_unit_choice == 0:
            graph2_y_list.append(turbine.get_T2a())
            graph2_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 4 and temp_unit_choice == 2:
            graph2_y_list.append(kelvin_to_celsius(turbine.get_T4a()))
            graph2_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 4 and temp_unit_choice == 1:
            graph2_y_list.append(kelvin_to_farenheit(turbine.get_T4a()))
            graph2_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 4 and temp_unit_choice == 0:
            graph2_y_list.append(turbine.get_T4a())
            graph2_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 5 and temp_unit_choice == 2:
            graph2_y_list.append(kelvin_to_celsius(turbine.get_T4s()))
            graph2_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 5 and temp_unit_choice == 1:
            graph2_y_list.append(kelvin_to_farenheit(turbine.get_T4s()))
            graph2_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 5 and temp_unit_choice == 0:
            graph2_y_list.append(turbine.get_T4s())
            graph2_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 6 and temp_unit_choice == 2:
            graph2_y_list.append(kelvin_to_celsius(turbine.get_Tb()))
            graph2_ax.set_ylabel("Degrees Celsius (C)")
            plot_data(plot_choice)
        elif plot_choice == 6 and temp_unit_choice == 1:
            graph2_y_list.append(kelvin_to_farenheit(turbine.get_Tb()))
            graph2_ax.set_ylabel("Degrees Farenheit (F)")
            plot_data(plot_choice)
        elif plot_choice == 6 and temp_unit_choice == 0:
            graph2_y_list.append(turbine.get_Tb())
            graph2_ax.set_ylabel("Kelvin (K)")
            plot_data(plot_choice)

        elif plot_choice == 7 and pressure_unit_choice == 0:
            graph2_y_list.append(turbine.get_P1())
            graph2_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 7 and pressure_unit_choice == 2:
            graph2_y_list.append(kpa_to_psi(turbine.get_P1()))
            graph2_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 7 and pressure_unit_choice == 3:
            graph2_y_list.append(kpa_to_bar(turbine.get_P1()))
            graph2_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 8 and pressure_unit_choice == 0:
            graph2_y_list.append(turbine.get_P2())
            graph2_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 8 and pressure_unit_choice == 1:
            graph2_y_list.append(kpa_to_psi(turbine.get_P2()))
            graph2_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 8 and pressure_unit_choice == 2:
            graph2_y_list.append(kpa_to_bar(turbine.get_P2()))
            graph2_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 9 and pressure_unit_choice == 0:
            graph2_y_list.append(turbine.get_P3())
            graph2_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 9 and pressure_unit_choice == 1:
            graph2_y_list.append(kpa_to_psi(turbine.get_P3()))
            graph2_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 9 and pressure_unit_choice == 2:
            graph2_y_list.append(kpa_to_bar(turbine.get_P3()))
            graph2_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 10 and pressure_unit_choice == 0:
            graph2_y_list.append(turbine.get_P4())
            graph2_ax.set_ylabel("Kilopascals (KPa)")
            plot_data(plot_choice)
        elif plot_choice == 10 and pressure_unit_choice == 1:
            graph2_y_list.append(kpa_to_psi(turbine.get_P4()))
            graph2_ax.set_ylabel("Pounds per Square Inch (PSI)")
            plot_data(plot_choice)
        elif plot_choice == 10 and pressure_unit_choice == 2:
            graph2_y_list.append(kpa_to_bar(turbine.get_P4()))
            graph2_ax.set_ylabel("Atmospheres (Bar)")
            plot_data(plot_choice)

        elif plot_choice == 11 and velocity_unit_choice == 0:
            graph2_y_list.append(turbine.get_Vb())
            graph2_ax.set_ylabel("Meters Per Second (m/s)")
            plot_data(plot_choice)
        elif plot_choice == 11 and velocity_unit_choice == 1:
            graph2_y_list.append(ms_to_mph(turbine.get_Vb()))
            graph2_ax.set_ylabel("Miles Per Hour (MPH)")
            plot_data(plot_choice)
        elif plot_choice == 11 and velocity_unit_choice == 2:
            graph2_y_list.append(ms_to_kph(turbine.get_Vb()))
            graph2_ax.set_ylabel("Kilometers Per Hour (KPH)")
            plot_data(plot_choice)

        elif plot_choice == 12 and KE_unit_choice == 0:
            graph2_y_list.append(turbine.get_KEbJ())
            graph2_ax.set_ylabel("Joules (J)")
            plot_data(plot_choice)
        elif plot_choice == 12 and KE_unit_choice == 1:
            graph2_y_list.append(turbine.get_KEbKJKG())
            graph2_ax.set_ylabel("Kilojoules Per Kilogram (KJ/KG)")
            plot_data(plot_choice)

        elif plot_choice == 13:
            graph2_y_list.append(turbine.get_thrust())
            graph2_ax.set_ylabel("Thrust (N)")
            plot_data(plot_choice)

        elif plot_choice == 14:
            graph2_y_list.append(latest_value)
            graph2_ax.set_ylabel("RPM")
            plot_data(plot_choice)

    #Plot data to graph
    def plot_data(plot_choice):
        graph2_x_list.append(i)
        graph2_ax.plot(graph2_x_list, graph2_y_list, color='r', label=plot_list[plot_choice])
        graph2_ax.legend()
        graph2_ax.set_title("Graph 2: " + plot_list[plot_choice] + " over Time")
        graph2_ax.set_xlabel("Time (s)")

    ani2.event_source.interval = SC.settings.config_list[9]

    graph2_ax.set_xlim(left=max(0, i - 50), right=i + 50)

    graph2_ax.clear()

    if graph2_old_choice == graph2_new_choice:
        choose_plot(graph2_new_choice)
    else:
        graph2_x_list.clear()
        graph2_y_list.clear()

        graph2_old_choice = graph2_new_choice

        choose_plot(graph2_new_choice)

#Display a popup window
def popup_warning(msg):
    top = tk.Toplevel()
    top.title("Warning!")
    top.geometry("340x120")
    top.resizable(width=False, height=False)
    top.bell()

    #Create image and place it in label for background
    popup_image_path = os.path.join(base_folder, 'images/popup_page_image.png')
    turbine_image = tk.PhotoImage(file=popup_image_path, master=top)
    turbine_image_l = tk.Label(top, image=turbine_image)
    turbine_image_l.image = turbine_image
    turbine_image_l.place(x=-2, y=-3)

    display_message = tk.StringVar()
    display_message.set(msg)

    #Widgets
    notification_l = tk.Label(top, textvariable=display_message, font=SMALL_FONT, wraplength=250)

    dismiss_button = tk.Button(top, text="Dismiss", command=top.destroy, relief='flat', activebackground="#20a6cb",
                       bg="#20a6cb")
    dismiss_button.config(overrelief="raised")

    #Place widgets onto page
    notification_l.place(relx=0.1, y=15)
    dismiss_button.place(x=120, y=70)

#Creates the "Set Refresh Rate" popup window
def set_refresh_popup(graph):
    #Get value from entry and save to settings
    def set_refresh():
        if graph == 1:
            SC.settings.config_list[8] = int(refresh_rate_e.get())
        else:
            SC.settings.config_list[9] = int(refresh_rate_e.get())

        #Write new settings to external file
        SC.settings.save_config()

        #Reload config
        SC.settings.load_config()

        #Get rid of popup window
        top.destroy()

    top = tk.Toplevel()
    top.title("Set Refresh Rate")
    top.geometry("300x100")
    top.resizable(width=False, height=False)
    top.bell()

    # Create image and place it in label for background
    refresh_image_path = os.path.join(base_folder, 'images/refresh_page_image.png')
    turbine_image = tk.PhotoImage(file=refresh_image_path, master=top)
    turbine_image_l = tk.Label(top, image=turbine_image)
    turbine_image_l.image = turbine_image
    turbine_image_l.place(x=-2, y=-3)

    #Widgets
    refresh_rate_l = tk.Label(top, text="Set refresh rate (ms):", font=SMALL_FONT)

    refresh_rate_e = tk.Entry(top, width=8)

    if graph == 1:
        refresh_rate_e.insert(0, SC.settings.config_list[8])
    else:
        refresh_rate_e.insert(0, SC.settings.config_list[9])

    set_refresh_rate_b = tk.Button(top, text="Set", command=set_refresh, relief='flat', activebackground="#20a6cb",
                                   bg="#20a6cb", width=10, font=SMALL_FONT)
    set_refresh_rate_b.config(overrelief="raised")

    #Place widgets onto page
    refresh_rate_l.place(x=10, y=25)
    refresh_rate_e.place(x=235, y=25)
    set_refresh_rate_b.place(x=100, y=60)

#Control which graphs are on/off
def control_graph_ani(graph, condition):
    if graph == 1:
        if not condition:
            ani1.event_source.stop()
        else:
            ani1.event_source.start()
    else:
        if not condition:
            ani2.event_source.stop()
        else:
            ani2.event_source.start()

#Load an existing turbine config into program
def load_settings():
    filename = filedialog.askopenfilename(title="Load Settings From File:", defaultextension=".txt",
                                          initialfile="SettingConfiguration")

#Take current turbine config and save it to external file
def save_settings():
    filename = filedialog.asksaveasfilename(title="Save Settings To File:", defaultextension=".txt",
                                            initialfile="SettingConfiguration")

#Create the "Preferences" popup window
def preferences_popup():

    #Get vales from entries and save them to settings
    def confirm():
        inputs_valid = True

        #Validate inputs and set config
        if (validate_int_input(nozzle_thrust_coeff_e.get(), 0.1, 100)):
            SC.settings.config_list[0] = int(nozzle_thrust_coeff_e.get())
        else:
            inputs_valid = False

        if (validate_int_input(combustor_pressure_loss_e.get(), 0.1, 100)):
            SC.settings.config_list[1] = int(combustor_pressure_loss_e.get())
        else:
            inputs_valid = False

        if (validate_int_input(jetpipe_pressure_loss_e.get(), 0.1, 100)):
            SC.settings.config_list[2] = int(jetpipe_pressure_loss_e.get())
        else:
            inputs_valid = False

        if (validate_int_input(ambient_temp_e.get(), 1, 10000)):
            SC.settings.config_list[3] = int(ambient_temp_e.get())
        else:
            inputs_valid = False

        if (validate_int_input(ambient_pressure_e.get(), 1, 1000)):
            SC.settings.config_list[4] = int(ambient_pressure_e.get())
        else:
            inputs_valid = False

        if (validate_int_input(combustor_output_temp_e.get(), 1, 10000)):
            SC.settings.config_list[5] = int(combustor_output_temp_e.get())
        else:
            inputs_valid = False

        if inputs_valid:
            #Write new settings to external file
            SC.settings.save_config()

            #Reload config
            SC.settings.load_config()

            #Set new turbine preferences
            update_turbine_preferences()

            #Get rid of popup window
            top.destroy()

    #Clear entries and enter default values
    def reset_preference_default_values():
        nozzle_thrust_coeff_e.delete(0, "end")
        combustor_pressure_loss_e.delete(0, "end")
        jetpipe_pressure_loss_e.delete(0, "end")
        ambient_temp_e.delete(0, "end")
        ambient_pressure_e.delete(0, "end")
        combustor_output_temp_e.delete(0, "end")

        nozzle_thrust_coeff_e.insert(0, SC.settings.default_values[0])
        combustor_pressure_loss_e.insert(0, SC.settings.default_values[1])
        jetpipe_pressure_loss_e.insert(0, SC.settings.default_values[2])
        ambient_temp_e.insert(0, SC.settings.default_values[3])
        ambient_pressure_e.insert(0, SC.settings.default_values[4])
        combustor_output_temp_e.insert(0, SC.settings.default_values[5])

    top = tk.Toplevel()
    top.title("Preferences")
    top.geometry("400x270")
    top.resizable(width=False, height=False)
    top.bell()

    # Create image and place it in label for background
    preferences_image_path = os.path.join(base_folder, 'images/preferences_page_image.png')
    turbine_image = tk.PhotoImage(file=preferences_image_path, master=top)
    turbine_image_l = tk.Label(top, image=turbine_image)
    turbine_image_l.image = turbine_image
    turbine_image_l.place(x=-2, y=-3)

    #Label widgets
    preferences_l = tk.Label(top, text="Preferences:", font=MIDDLE_FONT)
    nozzle_thrust_coeff_l = tk.Label(top, text="Nozzle Thrust Coefficient (%):", font=SMALL_FONT)
    combustor_pressure_loss_l = tk.Label(top, text="Combustor Pressure Loss (%):", font=SMALL_FONT)
    jetpipe_pressure_loss_l = tk.Label(top, text="Jetpipe Pressure Loss (%):", font=SMALL_FONT)
    ambient_temp_l = tk.Label(top, text="Ambient Temperature (K):", font=SMALL_FONT)
    ambient_pressure_l = tk.Label(top, text="Ambient Pressure (KPa):", font=SMALL_FONT)
    combustor_output_temp_l = tk.Label(top, text="Combustor Output Temp (K):", font=SMALL_FONT)

    #Entry widgets
    nozzle_thrust_coeff_e = tk.Entry(top, width=8)
    nozzle_thrust_coeff_e.insert(0, SC.settings.config_list[0])
    combustor_pressure_loss_e = tk.Entry(top, width=8)
    combustor_pressure_loss_e.insert(0, SC.settings.config_list[1])
    jetpipe_pressure_loss_e = tk.Entry(top, width=8)
    jetpipe_pressure_loss_e.insert(0, SC.settings.config_list[2])
    ambient_temp_e = tk.Entry(top, width=8)
    ambient_temp_e.insert(0, SC.settings.config_list[3])
    ambient_pressure_e = tk.Entry(top, width=8)
    ambient_pressure_e.insert(0, SC.settings.config_list[4])
    combustor_output_temp_e = tk.Entry(top, width=8)
    combustor_output_temp_e.insert(0, SC.settings.config_list[5])

    #Button widgets
    confirm_b = tk.Button(top, text="Confirm", command=confirm, relief='flat', activebackground="#20a6cb",
                          bg="#20a6cb", font=SMALL_FONT)
    confirm_b.config(overrelief="raised")
    reset_defaults_b = tk.Button(top, text="Reset Default Values", command=reset_preference_default_values,
                                 relief='flat', activebackground="#20a6cb", bg="#20a6cb", font=SMALL_FONT)
    reset_defaults_b.config(overrelief="raised")

    #Place widgets onto page
    preferences_l.place(x=132, y=10)
    nozzle_thrust_coeff_l.place(x=15, y=45)
    combustor_pressure_loss_l.place(x=15, y=65)
    jetpipe_pressure_loss_l.place(x=15, y=85)
    ambient_temp_l.place(x=15, y=105)
    ambient_pressure_l.place(x=15, y=125)
    combustor_output_temp_l.place(x=15, y=145)

    nozzle_thrust_coeff_e.place(x=330, y=45)
    combustor_pressure_loss_e.place(x=330, y=65)
    jetpipe_pressure_loss_e.place(x=330, y=85)
    ambient_temp_e.place(x=330, y=105)
    ambient_pressure_e.place(x=330, y=125)
    combustor_output_temp_e.place(x=330, y=145)

    confirm_b.place(x=300, y=200)
    reset_defaults_b.place(x=15, y=200)

#Set the turbine input preferences
def update_turbine_preferences():
    turbine.set_Ta(SC.settings.config_list[3])
    turbine.set_Pa(SC.settings.config_list[4])
    turbine.set_Pb(SC.settings.config_list[4])
    turbine.set_T3(SC.settings.config_list[5])

#Assign new plot choice to the respective "new_choice" global variables
def set_plot_choice(graph, selection):
    global graph1_new_choice, graph2_new_choice

    if graph == 1:
        graph1_new_choice = selection
    else:
        graph2_new_choice = selection

#Assign new unit choice to the respective "unit_choice" global variables
def set_unit_choice(selection, unit_menu_choice):
    global temp_unit_choice, pressure_unit_choice, velocity_unit_choice, KE_unit_choice

    if unit_menu_choice == 0:
        KE_unit_choice = selection
    elif unit_menu_choice == 1:
        temp_unit_choice = selection
    elif unit_menu_choice == 2:
        pressure_unit_choice = selection
    elif unit_menu_choice == 3:
        velocity_unit_choice = selection

#convert kelvin to degrees Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

#Convert kelvin to degrees Farenheit
def kelvin_to_farenheit(kelvin):
    return kelvin_to_celsius(kelvin) * (9 / 5) + 32

#Convert kilopascals to pounds per square inch
def kpa_to_psi(kpa):
    return kpa * 0.1450377377

#Convert kilopascals to bar
def kpa_to_bar(kpa):
    return kpa / 100

#Convert meters per second to miles per hour
def ms_to_mph(ms):
    return ms * 2.237

#Convert meters per second to kilometers per hour
def ms_to_kph(ms):
    return ms * 3.6

#Check input is a int and is within a range
def validate_int_input(value, min, max):
    try:
        value = int(value)

        if (value >= min and value <= max):
            return 1
        else:
            popup_warning("Enter a number between " + str(min) + " and " + str(max) + "!")

    except Exception as e:
        popup_warning("Enter a number between " + str(min) +" and " + str(max) + "!")

#Check input is a int and is within a range
def validate_float_input(value, min, max):
    try:
        value = float(value)

        if (value >= min and value <= max):
            return 1
        else:
            popup_warning("Enter a number between " + str(min) + " and " + str(max) + "!")

    except Exception as e:
        popup_warning("Enter a number between " + str(min) + " and " + str(max) + "!")

app = Start()

#Configure how window will fit onto screen
app.wm_state('zoomed')
width, height = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry('%dx%d+0+0' % (width,height))

#Create animation functions to update graphs
ani1 = animation.FuncAnimation(graph1, animate_graph1, interval=SC.settings.config_list[8])
ani2 = animation.FuncAnimation(graph2, animate_graph2, interval=SC.settings.config_list[9])

app.mainloop()
