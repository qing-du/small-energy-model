from oemof import solph
from oemof.outputlib import processing


import Network as nt


import os 
import pandas as pd

import oemof.graph as grph 


import matplotlib.pyplot as plt 


import networkx as nx











om = solph.Model(nt.energysystem)

om.solve(solver = 'cbc', solve_kwargs ={'tee':True})

my_results = processing.results(om)


#ax = plt.plot(nt.data['demand_el'])
#ax.set_xlabel('Date')
#ax.set_ylabel('Power demand')
#plt.show
