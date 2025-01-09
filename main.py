from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

backend = AerSimulator()

# AND
def and_gate(circuit, a, b, output):
    circuit.ccx(a, b, output)

# OR
def or_gate(circuit, a, b, output):
    circuit.cx(a, output)
    circuit.cx(b, output)
    circuit.ccx(a, b, output)

# XOR
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
    circuit.barrier()

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
    """
    reset_bits(bits=AUX)
    
    xor_gate(circuit=circuit, a=a, b=b, output=AUX[0])
    xor_gate(circuit=circuit, a=AUX[0], b=c_in, output=r)

    and_gate(circuit=circuit, a=a, b=b, output=AUX[1])
    and_gate(circuit=circuit, a=AUX[0], b=c_in, output=AUX[2])

    or_gate(circuit=circuit, a=AUX[1], b=AUX[2], output=c_out)



N_QUBITS = 10
circuit = QuantumCircuit(N_QUBITS, 2)

set_bits(circuit=circuit, A=[0, 1], X="00")
full_adder(circuit, a=0, b=1, c_in=2, c_out=3, r=4, AUX=[5, 6, 7])



circuit.measure([4, 3], [0,1])
print(circuit)

transpiled_circuit = transpile(circuit, backend)
n_shots = 1024
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)