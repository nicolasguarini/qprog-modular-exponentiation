from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from utilities import *
from functions import *

backend = AerSimulator()

## CREATE CIRCUIT
b = "10"
n = "11"
x = "10"
y = "00"

print(f"Doing {int(b,2)} * {int(x,2)}^{int(y,2)} mod {int(n,2)}")
print(f"Expected result: {int(b,2) * int(x,2)**int(y,2) % int(n,2)}")

B_register = range(len(b))

AUX = range(len(n), len(n)+(9 * len(n) + 6))

n_qubits = (8*len(n)+6) + (2*len(n))

circuit = QuantumCircuit(n_qubits, len(b))

set_bits(circuit=circuit, A=B_register, X="".join(reversed(b)))

multiply_mod_fixed_power_Y(circuit=circuit, N=n, X=x, B=B_register, AUX=AUX, Y=y)

circuit.measure(B_register, range(len(b)))
print(f"Running circuit({n_qubits}, {len(b)})")

## COMPILE AND RUN
transpiled_circuit = transpile(circuit, backend)
n_shots = 1
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)
