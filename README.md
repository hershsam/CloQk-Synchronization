# Motivation
The ability to measure time with high precision and accuracy is an essential requirement for not just scientific exploration but also for communication, navigation and a plethora of technological applications. 
Clock synchronization determines the time difference between spatially separated clocks. 
With the increasing popularity of quantum information, quantum entanglement promises to be a useful platform for several applications of communication. This is the spirit that we apply to our project, quantum clock synchronization.

Classically, clock synchronization algorithms either make use of a client-server model or they employ a decentralized approach where nodes coordinate directly with each other to align their clocks. In the client-server model, the client sends a request to a server (which has a more accurate clock), and the server responds with a time stamp. The client then estimates the round-trip network delay and adjusts its own clock accordingly. Algorithms like **Cristian’s Algorithm** and **Network Time Protocol (NTP)** work this way, where the client uses the server's timestamp along with the round-trip delay to adjust its local clock. In contrast, decentralized models like the **Berkeley Algorithm** allow nodes to synchronize their clocks with each other without relying on a single authoritative time server. In this model, one node acts as a coordinator, periodically requesting the time from other nodes, calculating the average time, and sending adjustment messages back to each node.

Classical clock synchronization protocols, while effective, face several challenges that can be addressed by quantum clock synchronization. One major issue is network delay, as classical protocols like NTP and Cristian’s algorithm rely on estimating round-trip time, which can be asymmetric and unpredictable. Quantum synchronization, using entangled particles, can avoid this by providing instantaneous and precise time transfer, regardless of network conditions. Furthermore, while classical systems struggle with maintaining accuracy over long distances, quantum entanglement allows for synchronization over vast distances without degradation, offering better scalability and precision, especially in large networks. 

# Working Principle
First consider a qubit with stationary states in the computational basis as $\ket{0}$ and $\ket{1}$. 
Starting with the initial state, a maximally entangled bell state:

$$\ket{\psi} = \frac{\ket{00}+ \ket{11}}{\sqrt{2}} = \frac{\ket{+}_A \ket{+}_B + \ket{-}_A \ket{-}_B}{\sqrt{2}}$$

Here A and B refer to the qubit distributed to Alice and Bob. Alice and Bob both measure their respective qubits at $t=0$. Their clocks being unsynchronized leads to Bob measuring the qubit later than Alice, with a gap of $\Delta$.

When Alice measures $\ket{+}$, Bob's qubit immediately collapses to $\ket{+}$. In the $\Delta$ between their measurements, Bob's state evolves with time : 
$$
\ket{\psi_B} = \frac {\ket{0} + e^{-i \omega \Delta}\ket{1}}{\sqrt{2}}
$$
Bob obtains $\ket{1}$ with probability
$$
P(\ket{+}) = \bra{+} \ket{\psi_B} = \frac{1 + cos(\omega \Delta)}{2}
$$
This probability allows Bob to sample and calculate for $\Delta$
# Algorithm Summary
This algorithm for multiparty clock synchronization is infitely scalable. This program implements this for two and three node networks.
* The initial state is a quantum W-state :

  $$\ket{\psi} = \frac{1}{\sqrt{n}}(\ket{10...00} + \ket{01...00} + \ket{00...01})$$
* Alice, at standard time $t_A = 0$ measures the qubit in her possession in the $(\ket{+},\ket{-})$ basis .
  - Alice is taken as the standard without loss of generality, and synchronization is performed relative to her clock.
* Alice broadcasts her measurement result across the network.
* Every node performs measurement based on their respective clocks at $t=0$, which has a difference of $\Delta$ from the standard clock.
* If Alice measured $\ket{+}$, the others obtain $\ket{+}$ upon measurement with probability:

$$P(\ket{+}) = \frac{1}{2} + \frac{cos(\omega \Delta)}{n}, \omega = \omega_2 ,\omega_3 ... , \omega_{n}$$
* Over many iterations, the others can deduce the value of $\Delta$.
  - For $|\omega \Delta|<2 \pi$, the others can adjust their clock accordingly.  
