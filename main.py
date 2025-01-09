from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

backend = AerSimulator()

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

N_QUBITS = 10
circuit = QuantumCircuit(N_QUBITS, 2)

set_bits(circuit=circuit, A=[0, 1], X="11")
copy(circuit=circuit, A=[0, 1], B=[2, 3])



circuit.measure([8,9], [0,1])
print(circuit)

transpiled_circuit = transpile(circuit, backend)
n_shots = 1024
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)