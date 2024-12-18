from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket
from netqasm.sdk.qubit import Qubit
import parameters
import squidasm.util.routines as routines
from squidasm.util import get_qubit_state
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta
import numpy


class AliceProgram(Program):
    
    #Alice's clock is considered as the standard, without loss of generality 

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=["Bob","Charlie"],
            epr_sockets=["Bob","Charlie"],
            max_qubits=10,
        )

    def run(self, context: ProgramContext):

        connection = context.connection

        qa = Qubit(connection)

        #Generating 3 qubit W-state (distributed across Alice, Bob and Charlie) : 

        qa.rot_Y(angle= 1.91063324)
        yield from routines.distributed_CPhase_control(context,"Bob",qa)
        yield from connection.flush()
        yield from routines.distributed_CNOT_control(context,"Bob",qa)
        qa.X()

        A = qa.measure()
        yield from connection.flush()

        # Alice broadcasts her result

        context.csockets["Charlie"].send(str(A))
        context.csockets["Bob"].send(str(A))

        return {}


class BobProgram(Program):
    # PEER_NAME = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=["Charlie","Alice"],
            epr_sockets=["Charlie","Alice"],
            max_qubits=10,
        )

    def run(self, context: ProgramContext):

        connection: BaseNetQASMConnection = context.connection

        qb = Qubit(connection)
        qb.rot_Y(7,2)
        yield from routines.distributed_CPhase_target(context,"Alice",qb)
        qb.rot_Y(1,2)

        yield from routines.distributed_CNOT_control(context,"Charlie",qb)
        yield from routines.distributed_CNOT_target(context,"Alice",qb)

        #Receiving Alice's measurement results
        A_qubit = yield from context.csockets["Alice"].recv()
        if int(A_qubit)==0 : return{}
        
        # Bob's qubit evolves in the time delay after Alice's measurement
        # This time evolution can be represented as a rotation in Z
        qb.H()
        qb.rot_Z(angle= parameters.wB*parameters.deltaB)
        qb.H()
        B = qb.measure()
        yield from connection.flush()

        # The distribution of Bob's measurements over many iterations is stored
        parameters.second = parameters.second +int(B)
        parameters.first = parameters.first + 1
        return {}

class CharlieProgram(Program):
    # PEER_NAME = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=["Alice","Bob"],
            epr_sockets=["Alice","Bob"],
            max_qubits=10,
        )

    def run(self, context: ProgramContext):

        connection: BaseNetQASMConnection = context.connection
        
        qc = Qubit(connection)
        yield from connection.flush()
        yield from routines.distributed_CNOT_target(context,"Bob",qc)
        yield from connection.flush()
        
        #Receiving Alice's measurement result
        A_qubit = yield from context.csockets["Alice"].recv()
        if int(A_qubit)==0 : return{}
        
        # Charlie's qubit evolving in time after Alice's measurement 
        qc.H()
        qc.rot_Z(angle=parameters.wC*parameters.deltaC)
        qc.H()
        C = qc.measure()
        yield from connection.flush()
        
        parameters.third = parameters.third + int(C)
        return {}
