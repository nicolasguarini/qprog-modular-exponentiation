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
    
    def test_full_adder(self):
        test = [
            [('0', '0', '0'), {'00': 1024}],  # 0 + 0 + 0 = 0 (c_out = 0, result = 0)
            [('0', '0', '1'), {'01': 1024}],  # 0 + 0 + 1 = 1 (c_out = 0, result = 1)
            [('0', '1', '0'), {'01': 1024}],  # 0 + 1 + 0 = 1 (c_out = 0, result = 1)
            [('0', '1', '1'), {'10': 1024}],  # 0 + 1 + 1 = 2 (c_out = 1, result = 0)
            [('1', '0', '0'), {'01': 1024}],  # 1 + 0 + 0 = 1 (c_out = 0, result = 1)
            [('1', '0', '1'), {'10': 1024}],  # 1 + 0 + 1 = 2 (c_out = 1, result = 0)
            [('1', '1', '0'), {'10': 1024}],  # 1 + 1 + 0 = 2 (c_out = 1, result = 0)
            [('1', '1', '1'), {'11': 1024}],  # 1 + 1 + 1 = 3 (c_out = 1, result = 1)
        ]

        for (a, b, c_in), expected_counts in test:
            circuit = QuantumCircuit(8, 2)
            set_bits(circuit, A=[0], X=a)
            set_bits(circuit, A=[1], X=b)
            set_bits(circuit, A=[2], X=c_in)

            full_adder(circuit, a=0, b=1, c_in=2, c_out=3, r=4, AUX=[5,6,7])
            circuit.measure([4,3], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)
            
    def test_add(self):
        tests = [
            [('00', '00'), {'00': 1024}],
            [('00', '01'), {'01': 1024}],
            [('01', '00'), {'01': 1024}],
            [('01', '01'), {'10': 1024}],
            [('10', '00'), {'10': 1024}],
            [('10', '01'), {'11': 1024}],
            [('11', '00'), {'11': 1024}],
            [('11', '01'), {'00': 1024}],
        ]

        for (a, b), expected_counts in tests:
            circuit = QuantumCircuit(11, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(b)))

            add(circuit, A=[0,1], B=[2,3], R=[4,5], AUX=[6,7,8,9,10])
            circuit.measure([4,5], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_subtract(self):
        tests = [
            [('00', '00'), {'00': 1024}],
            [('10', '00'), {'10': 1024}],
            [('11', '00'), {'11': 1024}],
            [('01', '00'), {'01': 1024}],
            [('10', '01'), {'01': 1024}],
            [('01', '01'), {'00': 1024}],
            [('11', '01'), {'10': 1024}],
            [('11', '11'), {'00': 1024}],
            [('10', '10'), {'00': 1024}],
        ]

        for (a, b), expected_counts in tests:
            circuit = QuantumCircuit(11, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(b)))

            subtract(circuit, A=[0,1], B=[2,3], R=[4,5], AUX=[6,7,8,9,10])
            circuit.measure([4,5], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            n_shots = 1024
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_greater_than_or_equal(self):
        n_shots = 1
        tests = [
            [('00', '00'), {'1': n_shots}],
            [('10', '00'), {'1': n_shots}],
            [('11', '00'), {'1': n_shots}],
            [('01', '00'), {'1': n_shots}],
            [('10', '01'), {'1': n_shots}],
            [('01', '01'), {'1': n_shots}],
            [('11', '11'), {'1': n_shots}],
            [('10', '10'), {'1': n_shots}],
            [('00', '01'), {'0': n_shots}],
            [('01', '10'), {'0': n_shots}],
            [('00', '11'), {'0': n_shots}],
            [('01', '11'), {'0': n_shots}],
        ]

        for (a, b), expected_counts in tests:
            circuit = QuantumCircuit(12, 1)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(b)))

            greater_than_or_equal(circuit, A=[0,1], B=[2,3], r=4, AUX=[5,6,7,8,9,10,11])
            circuit.measure([4], [0])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_add_mod(self):
        n_shots = 1

        tests = [
            [('00', '00', '00'), {'00': n_shots}],
            [('00', '11', '10'), {'01': n_shots}],
            [('01', '01', '11'), {'10': n_shots}],
            [('00', '01', '01'), {'00': n_shots}],
        ]

        for (a, b, n), expected_counts in tests:
            circuit = QuantumCircuit(18, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(b)))
            set_bits(circuit, A=[4,5], X="".join(reversed(n)))

            add_mod(circuit=circuit, A=[0,1], B=[2,3], N=[4,5], R=[6,7], AUX=range(8,8+2*len(a)+6))
            circuit.measure([6,7], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def times_two_mod(self):
        n_shots = 1

        tests = [
            [('00', '00'), {'00': n_shots}],
            [('01', '01'), {'00': n_shots}],
            [('01', '10'), {'00': n_shots}],
            [('01', '11'), {'10': n_shots}],
            [('00', '11'), {'00': n_shots}],
        ]

        for (a, n), expected_counts in tests:
            circuit = QuantumCircuit(18, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(n)))

            times_two_mod(circuit=circuit, A=[0,1], N=[2,3], R=[4,5], AUX=range(6,6+3*len(a)+6))
            circuit.measure([4,5], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_times_two_power_mod(self):
        n_shots = 1

        tests = [
            [("00", "00", 0), {'00': n_shots}],
            [("00", "01", 1), {'00': n_shots}],
            [("01", "10", 1), {'00': n_shots}],
            [("01", "11", 1), {'10': n_shots}],
            [("01", "11", 0), {'01': n_shots}],
        ]

        for (a, n, k), expected_counts in tests:
            circuit = QuantumCircuit(20, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(n)))

            times_two_power_mod(circuit=circuit, A=[0,1], N=[2,3], k=k, R=[4,5], AUX=range(6,6+4*len(a)+6))
            circuit.measure([4,5], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_multiply_mod(self):
        n_shots = 1

        tests = [
            [("00", "00", "00"), {'00': n_shots}],
            [("01", "10", "11"), {'10': n_shots}],
            [("01", "01", "01"), {'00': n_shots}],
            [("01", "10", "10"), {'00': n_shots}],
        ]

        for (a, b, n), expected_counts in tests:
            circuit = QuantumCircuit(26, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(a)))
            set_bits(circuit, A=[2,3], X="".join(reversed(b)))
            set_bits(circuit, A=[4,5], X="".join(reversed(n)))

            multiply_mod(circuit=circuit, A=[0,1], B=[2,3], N=[4,5], R=[6,7], AUX=range(8,8+6*len(a)+6))
            circuit.measure([6,7], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_multiply_mod_fixed(self):
        n_shots = 1

        tests = [
            [("00", "00", "00"), {'00': n_shots}],
            [("01", "10", "11"), {'10': n_shots}],
            [("01", "01", "01"), {'00': n_shots}],
            [("01", "10", "10"), {'00': n_shots}],
        ]

        for (b, x, n), expected_counts in tests:
            circuit = QuantumCircuit(26, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(b)))
            set_bits(circuit, A=[2,3], X="".join(reversed(n)))

            multiply_mod_fixed(circuit=circuit, N=[2,3], X=x, B=[0,1], AUX=range(4,4+(8*len(b)+6)))
            circuit.measure([0,1], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_multiply_mod_fixed_power_2_k(self):
        n_shots = 1
        
        tests = {
            [('00', '00', '00', 0), {'00': n_shots}],
            [('01', '01', '01', 0), {'00': n_shots}],
            [('01', '01', '10', 1), {'01': n_shots}],
            [('01', '01', '11', 1), {'01': n_shots}],
            [('01', '10', '10', 0), {'00': n_shots}],
        }

        for (b, x, n, k), expected_counts in tests:
            circuit = QuantumCircuit(26, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(b)))

            multiply_mod_fixed_power_2_k(circuit=circuit, N=n, X=x, B=[0,1], k=k, AUX=range(2, 2+(9*len(b)+6)), k=0)
            circuit.measure([0,1], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)

    def test_multiply_mod_fixed_power_Y(self):
        n_shots = 1
        
        tests = [
            [('00', '00', '00', '00'), {'00': n_shots}],
            [('00', '01', '00', '01'), {'00': n_shots}],
            [('01', '10', '01', '01'), {'00': n_shots}],
            [('10', '10', '00', '11'), {'10': n_shots}],
        ]

        for (b, x, y, n), expected_counts in tests:
            circuit = QuantumCircuit(26, 2)
            set_bits(circuit, A=[0,1], X="".join(reversed(b)))

            multiply_mod_fixed_power_Y(circuit=circuit, N=n, X=x, Y=y, B=[0,1], AUX=range(2, 2+(9*len(b)+6)))
            circuit.measure([0,1], [0,1])

            transpiled_circuit = transpile(circuit, backend)
            job_sim = backend.run(transpiled_circuit, shots=n_shots)
            result_sim = job_sim.result()
            counts = result_sim.get_counts(transpiled_circuit)

            self.assertEqual(counts, expected_counts)



if __name__ == '__main__':
    unittest.main()
