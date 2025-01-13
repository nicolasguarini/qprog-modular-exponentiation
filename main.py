from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from utilities import *
from functions import *

backend = AerSimulator(method="statevector")

## CREATE CIRCUIT
a = "001" # 1
#b = "010" # 2
n = "011" # 3
k=2

A_register = range(0, len(a))
#B_register = range(len(a), 2 * len(a))
N_register = range(len(a), 2*len(a))
R_register = range(2*len(a), 3*len(a))
AUX_times_two_mod = range(3*len(a), 3*len(a)+(3*len(a)+5+1))
AUX_times_two_power_mod = range(3*len(a), 3*len(a)+(4*len(a)+5+1))


circuit = QuantumCircuit(7*len(a)+6, len(a))
set_bits(circuit=circuit, A=A_register, X="".join(reversed(a)))
#set_bits(circuit=circuit, A=B_register, X="".join(reversed(b)))
set_bits(circuit=circuit, A=N_register, X="".join(reversed(n)))

#times_two_mod(circuit=circuit, N=N_register, A=A_register, R=R_register, AUX=AUX_times_two_mod)
times_two_power_mod(circuit=circuit, N=N_register, A=A_register, k=k, R=R_register, AUX=AUX_times_two_power_mod)

circuit.measure(R_register, range(len(a)))
print(f"Running circuit({7*len(a)+6}, {len(a)})")

## COMPILE AND RUN

transpiled_circuit = transpile(circuit, backend)
n_shots = 1
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)
