
# INPUT Parameters for qubit frequency and time delay between nodes

# Bob : Qubit frequency, time delay
freqB = 1e6  #INPUT
wB = freqB*6.28
deltaB = 1e-7  #INPUT

# Charlie : Qubit frequency, time delay
freqC = 1e6   #INPUT
wC = freqB*6.28
deltaC = 2e-7   #INPUT

# Adjust number of iterations
num_iters = 900  #INPUT

# Global variables to track results 
first = 0
second =0 
third = 0