import os
import matplotlib.pyplot as plt
import numpy as np

class SolarCollector:
    def __init__(self, efficiency, area, initial_temperature):
        self.efficiency = efficiency # captures heat transfer efficiency from sunlight into water. Could be broken down more to account for materials, etc.
        self.area = area
        self.water_temperature = initial_temperature  # initial temperature
    # ...
    def collect_energy(self, sunlight_intensity, flow_rate):
        energy_collected = self.efficiency * self.area * sunlight_intensity
        self.flow_rate = flow_rate
        # current_water_temp = self.water_temperature
        # Assuming the specific heat capacity of water is 4.18 J/(g*C) and the density of water is 1 g/cm^3
        if energy_collected > 0:
            self.water_temperature += energy_collected / (self.flow_rate * 1000 * 4.18)
        else:
            # Subtract a constant amount of heat from the water_temperature
            self.water_temperature -= (0.57864  * self.area * (self.water_temperature - 4)) / (self.flow_rate * 1000 * 4.18)  # 0.578 ~= thermal conductivity of water at 10°C in mW/m-K


class Pump:
    def __init__(self, flow_rate):
        self.flow_rate = flow_rate  # in liters per minute

class StorageTank:
    def __init__(self, volume, initial_temperature,thermal_efficiency):
        self.volume = volume
        self.temperature = initial_temperature
        self.thermal_efficiency = thermal_efficiency
    # ...
    def update_temperature(self, incoming_temperature, outgoing_temperature, flow_rate):
        # Calculate the mass of the water in the tank (assuming the density of water is 1 kg/l)
        mass = self.volume  # in kg

        # Calculate the energy of the incoming and outgoing water
        # (assuming the specific heat capacity of water is 4.18 J/(g*C) and the density of water is 1 g/cm^3)
        incoming_energy = flow_rate * incoming_temperature * 4.18 * 1000  # in J
        outgoing_energy = flow_rate * outgoing_temperature * 4.18 * 1000  # in J

        # Calculate the new temperature of the water in the tank
        tank_temp = self.temperature = (mass * self.temperature * 4.18 * 1000 + incoming_energy - outgoing_energy) / (mass * 4.18 * 1000)
        # self.temperature = tank_temp * self.thermal_efficiency

def get_user_input():
    # Get input from the user
    efficiency = float(input("Enter the efficiency of the solar collector: "))
    area = float(input("Enter the area of the solar collector (in square meters): "))
    flow_rate = float(input("Enter the flow rate of the pump (in liters per minute): "))
    volume = float(input("Enter the volume of the storage tank (in liters): "))
    thermal_efficiency = float(input("Enter the thermal efficiency of the storage tank: "))
    initial_temperature = float(input("Enter the initial temperature of the water (in degrees Celsius): "))
    sunlight_intensity = float(input("Enter the peak sunlight intensity (in watts per square meter): "))
    duration = int(input("Enter the duration of the simulation (in minutes): "))
    
    # Save the values to the input file for next time
    with open('input.txt', 'w') as file:
        file.write(f"{efficiency}\n{area}\n{flow_rate}\n{volume}\n{thermal_efficiency}\n{initial_temperature}\n{sunlight_intensity}\n{duration}")

    return efficiency, area, flow_rate, volume, thermal_efficiency, initial_temperature, sunlight_intensity, duration
def run_simulation():
     # Check if the input file exists
    if os.path.exists('input.txt'):
        # If it exists, ask the user if they want to use the values from the file
        use_file = input("Do you want to use the values from the file input.txt? Y/N: ")
        if use_file.lower() == 'y':
            file = open('input.txt','r')
            lines = file.readlines()
            efficiency = float(lines[0])
            area = float(lines[1])
            flow_rate = float(lines[2])
            volume = float(lines[3])
            thermal_efficiency = float(lines[4])
            initial_temperature = float(lines[5])
            sunlight_intensity = float(lines[6])
            duration = int(lines[7])
        else:
            efficiency, area, flow_rate, volume, thermal_efficiency, initial_temperature, sunlight_intensity, duration = get_user_input()
    else:
        efficiency, area, flow_rate, volume, thermal_efficiency, initial_temperature, sunlight_intensity, duration = get_user_input()
        
    # Create the components
    collector = SolarCollector(efficiency, area, initial_temperature)
    pump = Pump(flow_rate)
    tank = StorageTank(volume, initial_temperature,thermal_efficiency)

    # Create lists to store the time and temperature values
    time_values = []
    temperature_values = []
    sunlight_intensity_values = []

    # Run the simulation
    for i in range(duration):
        # Calculate the sunlight intensity as a function of time
        new_sunlight_intensity = (sunlight_intensity) * np.sin (i / 1440 * 2 * np.pi) # Sine function with a period of 1440 minutes (24 hours)
        new_sunlight_intensity = max(new_sunlight_intensity, 0)  # At night, the sunlight intensity is set to 0
        collector.collect_energy(new_sunlight_intensity, pump.flow_rate)
        amount_pumped = pump.flow_rate  # in liters
        tank.update_temperature(collector.water_temperature, tank.temperature, pump.flow_rate)
        
        # Store the current time and temperature
        time_values.append(i)
        temperature_values.append(tank.temperature)
        sunlight_intensity_values.append(new_sunlight_intensity)

    # Plot the temperature values against the time values
    plt.plot(time_values, temperature_values)
    # plt.plot(time_values, sunlight_intensity_values)
    plt.xlabel('Time (minutes)')
    plt.ylabel('Tank Temperature (degrees Celsius)')
    # plt.ylabel('Sunlight Intensity (Watts per square meter)')
    plt.title('Tank Temperature vs Time')
    plt.show()    
if __name__ == "__main__":
    run_simulation()

