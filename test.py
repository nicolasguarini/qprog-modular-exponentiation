import unittest
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from main import *

backend = AerSimulator()

class Test(unittest.TestCase):
    def test_and_gate(self):
        tests = [
            [(0,0), {'0': 1024}],
            [(0,1), {'0': 1024}],
            [(1,0), {'0': 1024}],
            [(1,1), {'1': 1024}],
        ]

        for (a, b), expected_counts in tests:
            circuit = QuantumCircuit(3, 1)

            if a:
                circuit.x(0)
            if b:
                circuit.x(1)

            and_gate(circuit, a=0, b=1, output=2)
            circuit.measure([2], [0])

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots = n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)
            
            self.assertEqual(counts, expected_counts)

    def test_or_gate(self):
        tests = [
            [(0,0), {'0': 1024}],
            [(0,1), {'1': 1024}],
            [(1,0), {'1': 1024}],
            [(1,1), {'1': 1024}],
        ]

        for (a, b), expected_counts in tests:
            circuit = QuantumCircuit(3, 1)

            if a:
                circuit.x(0)
            if b:
                circuit.x(1)

            or_gate(circuit, a=0, b=1, output=2)
            circuit.measure([2], [0])

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots = n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)
            
            self.assertEqual(counts, expected_counts)

    def test_xor_gate(self):
        tests = [
            [(0,0), {'0': 1024}],
            [(0,1), {'1': 1024}],
            [(1,0), {'1': 1024}],
            [(1,1), {'0': 1024}],
        ]

        for (a, b), expected_counts in tests:
            circuit = QuantumCircuit(3, 1)

            if a:
                circuit.x(0)
            if b:
                circuit.x(1)

        xor_gate(circuit, a=0, b=1, output=2)
        circuit.measure([2], [0])

        transpiled_circuit = transpile(circuit, backend)
        n_shots = 1024
        job_sim = backend.run(transpiled_circuit, shots = n_shots)
        result_sim = job_sim.result()
        counts = result_sim.get_counts(transpiled_circuit)
        
        self.assertEqual(counts, expected_counts)

if __name__ == '__main__':
    unittest.main()
