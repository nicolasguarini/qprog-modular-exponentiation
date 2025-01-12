from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from utilities import *
from functions import *

backend = AerSimulator()

## CREATE CIRCUIT
a = "001" # 1
b = "010" # 2
n = "011" # 5

A_register = range(0, len(a))
B_register = range(len(a), 2 * len(a))
N_register = range(2*len(a), 3*len(a))
R_register = range(3*len(a), 4*len(a))
AUX_add_mod = range(4*len(a), 4*len(a)+(2*len(a)+5+1))


circuit = QuantumCircuit(6*len(a)+6, len(a))
set_bits(circuit=circuit, A=A_register, X="".join(reversed(a)))
set_bits(circuit=circuit, A=B_register, X="".join(reversed(b)))
set_bits(circuit=circuit, A=N_register, X="".join(reversed(n)))

add_mod(circuit=circuit, N=N_register, A=A_register, B=B_register, R=R_register, AUX=AUX_add_mod)

circuit.measure(R_register, range(len(a)))
print(circuit)

## COMPILE AND RUN

transpiled_circuit = transpile(circuit, backend)
n_shots = 1
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)
