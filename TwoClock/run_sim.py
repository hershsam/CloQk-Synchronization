from application import AliceProgram, BobProgram
import params
from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
import numpy as np

# import network configuration from file
cfg = StackNetworkConfig.from_file("config.yaml")

# Create instances of programs to run
alice_program = AliceProgram()
bob_program = BobProgram()

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program}, num_times=params.num_iters)

print(params.ones,params.zeros)
cosB = 2*(params.zeros/(params.zeros+params.ones))-1
print(np.arccos(cosB)/params.wB)