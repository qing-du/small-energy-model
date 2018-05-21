from oemof import solph
from oemof.outputlib import processing


import Network as nt


om = solph.Model(nt.energysystem)

om.solve(solver = 'cbc', solve_kwargs ={'tee':True})

my_results = processing.results(om)

