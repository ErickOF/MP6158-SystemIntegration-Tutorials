# **Tutorial 2 - SIP schematic simulation for AD5940 component in Keysight ADS**

## 1. Instrucciones generales
In this task, you must design and simulate the routing for the load of the
AD5940 component, where the critical pins CE0 and AIN1 are the ones that allow
the impedance of the load to be measured. These pins are connected through VIP
(Via-In-Pad) type vias and are routed through two layers, as described in the
following figure:

![image](https://github.com/ErickOF/MP6158-SystemIntegration-Tutorials/blob/main/src/img/tutorial2_figure.png)

The simulation of the PCB with the vias and routing allows obtaining the *S*
parameters of this connection, in a frequency range between 4.5 GHz and 5.5
GHz.

The schematic simulation must be performed in the Keysight ADS program, which
allows each part of this design to be simulated with blocks from the standard
library.

The component **library** will be evaluated in ADS with the schematic and the
substrate, and the simulation at the schematic level.
