# **Tutorial 3 - SIP electromagnetic simulation for the AD5940 component in Keysight ADS**

Continuing with the design of a SiP for the AD5940 component, in the previous
tutorial a schematic model was made to determine the S parameters of the
connection shown:


![image](https://github .com/ErickOF/MP6158-SystemIntegration-Tutorials/blob/main/src/img/tutorial3_figure.png)


A schematic simulation uses **concentrated parameter simulation models**,
which are equivalent circuits, based on mathematical equations for the
configurations of transmission lines (microstrip, stripline, etc.), pads,
resistors, among others. These models are theoretical.


The objective of this third tutorial is to create an **electromagnetic
simulation** model, which is different from the previous one, because it
incorporates elements such as the permittivity of the substrate and the loss
tangent, parasitic capacitance in the interconnections, magnetic permeability,
and the pattern can be obtained of radiation from the complete packaging.


The project **library** in ADS will be evaluated with the electromagnetic
simulation and the results in the form of S-parameter plots.

