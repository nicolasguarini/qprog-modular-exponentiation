from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

backend = AerSimulator()

def and_gate(circuit, a, b, output):
    circuit.ccx(a, b, output)


def or_gate(circuit, a, b, output):
    circuit.cx(a, output)
    circuit.cx(b, output)
    circuit.ccx(a, b, output)


def xor_gate(circuit, a, b, output):
    circuit.cx(a, output)
    circuit.cx(b, output)


def reset_bits(bits):
    for i in bits:
        circuit.reset(i)


def set_bits(circuit, A, X):
    """
    The function set_bits(circuit,A,X) initializes the bits of register A with the binary
    string X. In other words, for each i in len(X), if X[i]=1, then the function applies the
    X-gate to qubits[i]. Otherwise, it does nothing. Assume len(A)=len(X). For instance, if
    qubits = [2,4,3,7,5] and X = 01011, then you will apply an X-gate to the qubits 4, 7
    and 5.
    """
    for i in range(len(X)):
        if X[i] == '1':
            circuit.x(A[i])


def copy(circuit, A, B):
    """
    Function copy(circuit,A,B) copies the binary string bin(A) to register B. Assume that
    len(A)=len(B) and that before the application of the function, B is initialized to |0⟩. Hint:
    use CNOT gates.

    The function is correct because A and B are quantum registers, not binary strings. 
    copy(circuit, A, B) uses CNOT gates to transfer the quantum state of each qubit in A to the corresponding qubit in B, 
    preserving superpositions and entanglement. If A were a binary string, CNOT would not be applicable.
    """
    for i in range(len(A)):
        circuit.cx(A[i], B[i])
    circuit.barrier()


def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    """
    Function full_adder(circuit,a,b,r,c_in,c_out,AUX) implements a full adder (Figure
    3). The registers a and b store the bits to be added, c_in stores the carry-in bit, c_out
    stores the carry-out bit, r stores the result of the sum, and AUX is the auxiliary register.

    Needs len(AUX)=3.
    """
    reset_bits(bits=AUX)
    
    xor_gate(circuit=circuit, a=a, b=b, output=AUX[0])
    xor_gate(circuit=circuit, a=AUX[0], b=c_in, output=r)

    and_gate(circuit=circuit, a=a, b=b, output=AUX[1])
    and_gate(circuit=circuit, a=AUX[0], b=c_in, output=AUX[2])

    or_gate(circuit=circuit, a=AUX[1], b=AUX[2], output=c_out)

    reset_bits(bits=AUX)


def add(circuit, A, B, R, AUX):
    """
    Function add(circuit,A,B,R,AUX) implements a circuit that adds number(A) to number(B)
    and stores the result at register R. Assume that len(A)=len(B)=len(R). Such a circuit is
    obtained by creating a cascade of full-adder circuits, as specified in Figure 5. The carry bits
    are part of the auxiliary register AUX. Note that the carry-in bit of the first adder (from right
    to left) is set to 0.

    Needs 3 * len(A) + 5 total qubits
    Needs len(AUX)=5
    """
    l = len(A)

    A = "".join(reversed(A))
    B = "".join(reversed(B))

    set_bits(circuit=circuit, A=range(0, l), X=A)
    set_bits(circuit=circuit, A=range(l, 2*l), X=B)

    reset_bits(AUX)

    for i in range(l):
        if i%2 == 0:
            full_adder(circuit=circuit, a=i, b=i+l, r=R[i], c_in=AUX[0], c_out=AUX[1], AUX=AUX[2:])
        else:
            full_adder(circuit=circuit, a=i, b=i+l, r=R[i], c_in=AUX[1], c_out=AUX[0], AUX=AUX[2:])

    reset_bits(AUX)
   
    
## CREATE CIRCUIT
N_QUBITS = 11
circuit = QuantumCircuit(N_QUBITS, 2)

# set_bits(circuit=circuit, A=[0, 1], X="00")
# full_adder(circuit, a=0, b=1, c_in=2, c_out=3, r=4, AUX=[5, 6, 7])
add(circuit=circuit, A="11", B="11", R=[9,10], AUX=[4, 5, 6, 7, 8]) # Needs (3 * len(A)) + 5 qubits

## MEASURE AND PRINT CIRCUIT
circuit.measure([9,10], [0,1])
print(circuit)

## COMPILE AND RUN
transpiled_circuit = transpile(circuit, backend)
n_shots = 1024
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)