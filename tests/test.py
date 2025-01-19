import unittest
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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
    
    def test_set_bits(self):
        tests = [
            ["0101", [0, 1, 2, 3]],
            ["1010", [0, 1, 2, 3]],
            ["1100", [0, 1, 2, 3]],
            ["0011", [0, 1, 2, 3]],
        ]

        for X, A in tests:
            circuit = QuantumCircuit(4, 4)
            set_bits(circuit, A, X="".join(reversed(X)))
            circuit.measure(A, A)

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            expected_counts = {X: n_shots}
            self.assertEqual(counts, expected_counts)

    def test_copy(self):
        tests = [
            ["0101", [0, 1, 2, 3], [4, 5, 6, 7]],
            ["1010", [0, 1, 2, 3], [4, 5, 6, 7]],
            ["1100", [0, 1, 2, 3], [4, 5, 6, 7]],
            ["0011", [0, 1, 2, 3], [4, 5, 6, 7]],
        ]

        for X, A, B in tests:
            circuit = QuantumCircuit(8, len(X))
            set_bits(circuit, A, X="".join(reversed(X)))
            copy(circuit, A, B)
            circuit.measure(B, range(len(X)))

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            expected_counts = {X: n_shots}
            self.assertEqual(counts, expected_counts)
    
            
if __name__ == '__main__':
    unittest.main()
