from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket
from netqasm.sdk.qubit import Qubit
import params
from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta


class AliceProgram(Program):
    PEER_NAME = "Bob"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=1,
        )

    def run(self, context: ProgramContext):
        # get classical socket to peer
        csocket = context.csockets[self.PEER_NAME]
        epr_socket = context.epr_sockets[self.PEER_NAME]
        connection = context.connection

        #Create an EPR pair between Alice and Bob
        epr_qubit = epr_socket.create_keep()[0]

        result = epr_qubit.measure()
        yield from connection.flush()


        message = str(result)
        csocket.send(message)

        return {}


class BobProgram(Program):
    PEER_NAME = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="tutorial_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=1,
        )

    def run(self, context: ProgramContext):
        # get classical socket to peer
        csocket: Socket = context.csockets[self.PEER_NAME]
        # get EPR socket to peer
        epr_socket: EPRSocket = context.epr_sockets[self.PEER_NAME]
        # get connection to quantum network processing unit
        connection: BaseNetQASMConnection = context.connection
                
        epr_qubit = epr_socket.recv_keep()[0]
        yield from connection.flush()
        message = yield from csocket.recv()
        
        epr_qubit.H()
        epr_qubit.rot_Z(angle=params.wB*params.deltaB)
        epr_qubit.H()

        post = epr_qubit.measure()
        yield from connection.flush()
        if str(message)=="0":
            if int(post)==1 : params.ones=params.ones+1
            else : params.zeros=params.zeros+1

        return {}
