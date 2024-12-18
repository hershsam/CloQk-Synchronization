from application import AliceProgram, BobProgram, CharlieProgram
import numpy as np
from squidasm.run.stack.config import StackNetworkConfig
from squidasm.run.stack.run import run
import parameters
# import network configuration from file
cfg = StackNetworkConfig.from_file("config.yaml")

# Create instances of programs to run
alice_program = AliceProgram()
bob_program = BobProgram()
charlie_program = CharlieProgram()

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program, "Charlie": charlie_program}, num_times=parameters.num_iters)

cosB = 1 -2*parameters.second/parameters.first
cosC = 1 -2*parameters.third/parameters.first

print(f"Time delay to Bob : {np.arccos(cosB)/parameters.wB}")
print(f"Time delay to Charlie : {np.arccos(cosC)/parameters.wC}")