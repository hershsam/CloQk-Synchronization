# Motivation
The ability to measure time with high precision and accuracy is an essential requirement for not just scientific exploration but also for communication, navigation and a plethora of technological applications. 
Clock synchronization determines the time difference between spatially separated clocks. 
With the increasing popularity of quantum information, quantum entanglement promises to be a useful platform for several applications of communication. This is the spirit that we apply to our project, quantum clock synchronization.

# Application
First consider a qubit with stationary states in the computational basis as $\ket{0}$ and $\ket{1}$. We introduce the Hadamard basis with states $\ket{+} = \frac{\ket{0} + \ket{1}}{\sqrt{2}}$ and $\ket{-} = \frac{\ket{0} - \ket{1}}{\sqrt{2}}$. At the beginning of our application, we prepare the initial entangled state:
$\ket{\psi} = \frac{\ket{00}+ \ket{11}}{\sqrt{2}} = \frac{\ket{+}_A \ket{+}_B + \ket{-}_A \ket{-}_B}{\sqrt{2}}$
Here A and B refer to the qubit distributed to Alice and Bob. Assuming Alice's clock as the standard, once Alice measures 

# Algorithm Summary
This algorithm for multiparty clock synchronization is infitely scalable. This program implements this for two and three node networks.
* The initial state is a quantum W-state :
  $$\ket{\psi} = \frac{1}{\sqrt{n}}(\ket{10...00} + \ket{01...00} + \ket{00...01})$$
* Alice, at standard time $t_A = 0$ measures the qubit in her possession in the $(\ket{+},\ket{-})$ basis .
  - Alice is taken as the standard without loss of generality, and synchronization is performed relative to her clock.
* Alice broadcasts her measurement result across the network.
* Every node performs measurement based on their respective clocks at $t=0$, which has a difference of $\Delta$ from the standard clock.
* If Alice measured $\ket{+}$, the others obtain $\ket{+}$ upon measurement with probability:
$$ P(\ket{+}) = \frac{1}{2} + \frac{cos(\omega \Delta)}{n}, \omega = \omega_2 ,\omega_3 ... , \omega_n $$
* Over many iterations, the others can deduce the value of $\Delta$.
  - For $|\omega \Delta|<2 \pi$, the others can adjust their clock accordingly.  
