from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from utilities import *
from functions import *

backend = AerSimulator()

## CREATE CIRCUIT
#a = "11"
b = "10"
n = "11"
x = "10"
y = "00"
# k = 0

print(f"Doing {int(b,2)} * {int(x,2)}^{int(y,2)} mod {int(n,2)}")
print(f"Expected result: {int(b,2) * int(x,2)**int(y,2) % int(n,2)}")

#A_register = range(0, len(a))
B_register = range(len(b))
# N_register = range(len(b), 2 * len(b))
# AUX_times_two_mod = range(3*len(b), 3*len(b)+(3*len(b)+5+1))
# AUX_times_two_power_mod = range(3*len(b), 3*len(b)+(4*len(b)+5+1))
# AUX_multiply_mod = range(4*len(b), 4*len(b)+(6*len(b)+5+1))
# AUX_multiply_mod_fixed = range(2 * len(b), 2 * len(b)+(8 * len(b) + 6))
# AUX_multiply_xy_mod = range(len(b), len(b)+(9 * len(b) + 6))
AUX_multiply_xy_mod = range(len(n), len(n)+(9 * len(n) + 6))

#n_qubits_multiply_mod = 10 * len(b) + 6
# n_qubits_multiply_mod_fixed = (8*len(b)+6) + (2*len(b))
# n_qubits_multiply_mod_fixed = (8*len(b)+6) + (2*len(b))
n_qubits_multiply_xy_mod = (8*len(n)+6) + (2*len(n))

circuit = QuantumCircuit(n_qubits_multiply_xy_mod, len(b))
#set_bits(circuit=circuit, A=A_register, X="".join(reversed(a)))
set_bits(circuit=circuit, A=B_register, X="".join(reversed(b)))
# set_bits(circuit=circuit, A=N_register, X="".join(reversed(n)))

#times_two_mod(circuit=circuit, N=N_register, A=A_register, R=R_register, AUX=AUX_times_two_mod)
#times_two_power_mod(circuit=circuit, N=N_register, A=A_register, k=k, R=R_register, AUX=AUX_times_two_power_mod)
#multiply_mod_fixed(circuit=circuit, N=N_register, X=x, B=B_register, AUX=AUX_multiply_mod_fixed)
# multiply_mod_fixed_power_2_k(circuit=circuit, N=n, X=x, B=B_register, AUX=AUX_multiply_xy_mod, k=k)
multiply_mod_fixed_power_Y(circuit=circuit, N=n, X=x, B=B_register, AUX=AUX_multiply_xy_mod, Y=y)

circuit.measure(B_register, range(len(b)))
print(f"Running circuit({n_qubits_multiply_xy_mod}, {len(b)})")

## COMPILE AND RUN

transpiled_circuit = transpile(circuit, backend)
n_shots = 1
job_sim = backend.run(transpiled_circuit, shots = n_shots)

result_sim = job_sim.result()
counts = result_sim.get_counts(transpiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts: ", counts)
print("Probabilities: ", probs)
