from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# https://gist.github.com/primaryobjects/49674b30f1882401b32fc46d1991ef89

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

def controlled_and_gate(circuit, c, a, b, output):
    circuit.mcx([c, a, b], output)


def controlled_or_gate(circuit, c, a, b, output):
    circuit.mcx([c, a], output)
    circuit.mcx([c, b], output)
    circuit.mcx([c, a, b], output)


def controlled_xor_gate(circuit, c, a, b, output):
    circuit.mcx([c, a], output)
    circuit.mcx([c, b], output)


def main():
    N_QUBITS = 4
    circuit = QuantumCircuit(N_QUBITS, 1)

    # SET BITS
    circuit.x(0) # a
    circuit.x(1) # b
    circuit.x(2) # c
    circuit.barrier()

    # MEASURE
    controlled_or_gate(circuit, a=0, b=1, c=2, output=3)
    circuit.measure([3], [0])

    print(circuit)

    transpiled_circuit = transpile(circuit, backend)
    n_shots = 1024
    job_sim = backend.run(transpiled_circuit, shots = n_shots)

    result_sim = job_sim.result()
    counts = result_sim.get_counts(transpiled_circuit)
    probs = {key:value/n_shots for key,value in counts.items()}
    print("Counts: ", counts)
    print("Probabilities: ", probs)

if __name__ == "__main__":
    main()
