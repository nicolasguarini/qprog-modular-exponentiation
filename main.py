from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from utilities import *
from functions import *

backend = AerSimulator()

## CREATE CIRCUIT
a = "11"
b = "01"
n = "10" # (3*1) mod 2 = 1

A_register = range(0, len(a))
B_register = range(len(a), 2 * len(a))
N_register = range(2 * len(a), 3 * len(a))
R_register = range(3 * len(a), 4 *len(a))
AUX_times_two_mod = range(3*len(a), 3*len(a)+(3*len(a)+5+1))
AUX_times_two_power_mod = range(3*len(a), 3*len(a)+(4*len(a)+5+1))
AUX_multiply_mod = range(4*len(a), 4*len(a)+(6*len(a)+5+1))

n_qubits_multiply_mod = 10*len(a)+6

circuit = QuantumCircuit(n_qubits_multiply_mod, len(a))
set_bits(circuit=circuit, A=A_register, X="".join(reversed(a)))
set_bits(circuit=circuit, A=B_register, X="".join(reversed(b)))
set_bits(circuit=circuit, A=N_register, X="".join(reversed(n)))

#times_two_mod(circuit=circuit, N=N_register, A=A_register, R=R_register, AUX=AUX_times_two_mod)
#times_two_power_mod(circuit=circuit, N=N_register, A=A_register, k=k, R=R_register, AUX=AUX_times_two_power_mod)
multiply_mod(circuit=circuit, N=N_register, A=A_register, B=B_register, R=R_register, AUX=AUX_multiply_mod)

circuit.measure(R_register, range(len(a)))
print(f"Running circuit({n_qubits_multiply_mod}, {len(a)})")

## COMPILE AND RUN

transpiled_circuit = transpile(circuit, backend)
n_shots = 1
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)
