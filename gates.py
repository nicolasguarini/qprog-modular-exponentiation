from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# https://gist.github.com/primaryobjects/49674b30f1882401b32fc46d1991ef89

backend = AerSimulator()

N_QUBITS = 3
circuit = QuantumCircuit(N_QUBITS, 1)


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

# SET BITS
circuit.x(0)
circuit.x(1)
circuit.barrier()

# MEASURE
xor_gate(circuit, 0, 1, 2)
circuit.measure([2], [0])



print(circuit)

transpiled_circuit = transpile(circuit, backend)
n_shots = 1024
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)