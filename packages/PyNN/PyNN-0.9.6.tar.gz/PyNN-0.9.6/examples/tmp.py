"""Test of IfCurDelta model"""

import matplotlib.pyplot as plt
#import pyNN.spiNNaker as sim
import pyNN.nest as sim

#from spynnaker8.extra_models import IFCurDelta

sim.setup(timestep=0.01, min_delay=0.5, spike_precision="off_grid")

#p = sim.Population(5, IFCurDelta())
p = sim.Population(5, sim.IF_curr_delta())
#p = sim.Population(5, sim.IF_curr_exp())

e_input = sim.Population(1, sim.SpikeSourceArray(spike_times=[5, 15, 25]))
i_input = sim.Population(1, sim.SpikeSourceArray(spike_times=[10, 20]))

e_prj = sim.Projection(e_input, p, sim.AllToAllConnector(), sim.StaticSynapse(weight=5.0, delay=0.5), receptor_type="excitatory")
i_prj = sim.Projection(i_input, p, sim.AllToAllConnector(), sim.StaticSynapse(weight=-5.0, delay=0.5), receptor_type="inhibitory")


p.record('v')

sim.run(40.0)

vm = p.get_data().segments[0].analogsignals[0]

plt.plot(vm.times, vm)
plt.xlabel("ms")
plt.ylabel("mV")

plt.savefig("Results/if_curr_delta_test.png")

sim.end()
