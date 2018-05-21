# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers
import oemof.solph as solph

# import oemof base classes to create energy system objects
import logging
import os
import pandas as pd
import warnings

solver = 'cbc'  # 'glpk', 'gurobi',....
debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
solver_verbose = False  # show/hide solver output

############
# 1 initialize energysystem
############
date_time_index = pd.date_range('1/1/2018', periods = 8760, freq = 'H' )

energysystem = solph.EnergySystem(timeindex=date_time_index)




###########
# 2 Built the network
##########

# Create all Buses
bcoal = solph.Bus(label = "coal") 

bgas = solph.Bus(label = "gas")

bel = solph.Bus(label = "electricity")

# add all Buses to the EnergySystem

energysystem.add(bcoal, bgas, bel)

# create simple sink object for electrical demand for each electrical bus
solph.Sink(label='demand_elec', inputs={bel: solph.Flow(
       actual_value= data['demand_el'], fixed=True, nominal_value=1)})


# Create all Transformers

#create simple transformer object representing a gas power plant
energysystem.add(solph.Transformer(
    label="pp_gas",
    inputs={bgas: solph.Flow()},
    outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
    conversion_factors={bel: 0.58}))

energysystem.add(solph.Transformer(
       label="pp_coal", 
       inputs={bcoal: solph.Flow()}, 
       outputs = {bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
       conversion_factor ={bel:0.4}))


