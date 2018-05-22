# Default logger of oemof
from oemof.tools import logger
from oemof.tools import helpers
import oemof.solph as solph
from oemof.tools import economics

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




filename = os.path.join(os.path.dirname(__file__), 'basic_example.csv')
data = pd.read_csv(filename)


###########
# 2 Built the network
##########

# Create all Buses
bcoal = solph.Bus(label = "coal") 

bgas = solph.Bus(label = "gas")

bel = solph.Bus(label = "electricity")

# add all Buses to the EnergySystem

energysystem.add(bcoal, bgas, bel)


# create source object representing the natural gas commodity (annual limit)
energysystem.add(solph.Source(label='rgas', outputs={bgas: solph.Flow(
    nominal_value=10000000, variable_costs = 40)}))

# create source object representing the natural coal commodity (annual limit)
energysystem.add(solph.Source(label='rcoal', outputs={bcoal: solph.Flow(
    nominal_value=100000, variable_costs = 10)}))

# source wind
energysystem.add(solph.Source(label='wind', outputs={bel: solph.Flow(fixed=True, 
        actual_value=data['wind'], nominal_value=100000)}))

# create simple sink object for electrical demand for each electrical bus
solph.Sink(label='demand_elec', inputs={bel: solph.Flow(
       actual_value= data['demand_el'], fixed=True, nominal_value=1)})


# Create all Transformers

#create simple transformer object representing a gas power plant

epc_gas = economics.annuity(capex=1000, n=20, wacc=0.05)

energysystem.add(solph.Transformer(
    label="pp_gas",
    inputs={bgas: solph.Flow()},
    outputs={bel: solph.Flow(nominal_value = None, variable_costs=10,investment=solph.Investment(ep_costs=epc_gas))},
    conversion_factors={bel: 0.58}))

epc_coal = economics.annuity(capex=1000, n=60, wacc=0.05)

energysystem.add(solph.Transformer(
       label="pp_coal", 
       inputs={bcoal: solph.Flow()}, 
       outputs = {bel: solph.Flow(nominal_value = None, variable_costs=6,investment=solph.Investment(ep_costs=epc_coal))},
       conversion_factors ={bel:0.5}))


