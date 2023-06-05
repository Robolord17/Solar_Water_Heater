# Solar_Water_Heater
A python model simulation of heat transfer in a simple solar water heater system
When you run the program from the command terminal, it will ask you for input on the essential parameters.
It will then output a plot of the tank temperature vs time.

### With additional time, potential improvements would be:
* Getting real, local sunlight data (import based on user-entered location. Could also be fetched automatically based on IP address)
* More in-depth modeling of heat transfer at the solar collector. This could allow for modeling different materials and configurations for maximizing heat transfer efficiency.
* Adding controls sequencing to the pump. I assumed the pump was a forcing function defining a flow-rate through the system, but you could optimize flow rate for heat transfer, have start/stop conditions based on water temperature, etc.
* Modeling heat losses along pipe length: assuming insulation, this could be minimized.
* Modeling convective heat transfer in the tank.Allow for the user to input different fluids. I assumed this was a direct water heating system, but depending on the user entered location, the program could recommend glycol blends for an indirect system to reduce the risk of freezing.
* Allow the user to customize different set-ups to run models for direct/indirect solar water heaters, or passive/active systems, adding control valves, or different piping configurations.
