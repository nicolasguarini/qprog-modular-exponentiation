from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

backend = AerSimulator()

def and_gate(circuit, a, b, output):
    circuit.ccx(a, b, output)


def or_gate(circuit, a, b, output):
    circuit.cx(a, output)
    circuit.cx(b, output)
    circuit.ccx(a, b, output)


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


def reset_bits(bits):
    for i in bits:
        circuit.reset(i)


def set_bits(circuit, A, X):
    """
    The function set_bits(circuit,A,X) initializes the bits of register A with the binary
    string X. In other words, for each i in len(X), if X[i]=1, then the function applies the
    X-gate to qubits[i]. Otherwise, it does nothing. Assume len(A)=len(X). For instance, if
    qubits = [2,4,3,7,5] and X = 01011, then you will apply an X-gate to the qubits 4, 7
    and 5.
    """
    for i in range(len(X)):
        if X[i] == '1':
            circuit.x(A[i])


def copy(circuit, A, B):
    """
    Function copy(circuit,A,B) copies the binary string bin(A) to register B. Assume that
    len(A)=len(B) and that before the application of the function, B is initialized to |0⟩. Hint:
    use CNOT gates.

    The function is correct because A and B are quantum registers, not binary strings. 
    copy(circuit, A, B) uses CNOT gates to transfer the quantum state of each qubit in A to the corresponding qubit in B, 
    preserving superpositions and entanglement. If A were a binary string, CNOT would not be applicable.
    """
    for i in range(len(A)):
        circuit.cx(A[i], B[i])
    circuit.barrier()

def controlled_copy(circuit, control, A, B):
    for i in range(len(A)):
        circuit.ccx(control, A[i], B[i])


def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    """
    Function full_adder(circuit,a,b,r,c_in,c_out,AUX) implements a full adder (Figure
    3). The registers a and b store the bits to be added, c_in stores the carry-in bit, c_out
    stores the carry-out bit, r stores the result of the sum, and AUX is the auxiliary register.

    Needs len(AUX)=3.
    """
    reset_bits(bits=AUX)
    circuit.reset(c_out) # !! c_out must be 0 at the beginning
    
    xor_gate(circuit=circuit, a=a, b=b, output=AUX[0])
    xor_gate(circuit=circuit, a=AUX[0], b=c_in, output=r)

    and_gate(circuit=circuit, a=a, b=b, output=AUX[1])
    and_gate(circuit=circuit, a=AUX[0], b=c_in, output=AUX[2])

    or_gate(circuit=circuit, a=AUX[1], b=AUX[2], output=c_out)

    reset_bits(bits=AUX)


def controlled_full_adder(circuit, control, a, b, r, c_in, c_out, AUX):
    reset_bits(bits=AUX)
    circuit.reset(c_out) # !! c_out must be 0 at the beginning
    
    controlled_xor_gate(circuit=circuit, c=control, a=a, b=b, output=AUX[0])
    controlled_xor_gate(circuit=circuit, c=control, a=AUX[0], b=c_in, output=r)

    controlled_and_gate(circuit=circuit, c=control, a=a, b=b, output=AUX[1])
    controlled_and_gate(circuit=circuit, c=control, a=AUX[0], b=c_in, output=AUX[2])

    controlled_or_gate(circuit=circuit, c=control, a=AUX[1], b=AUX[2], output=c_out)

    reset_bits(bits=AUX)


def add(circuit, A, B, R, AUX):
    # Needs len(AUX)=5

    l = len(A)
    reset_bits(bits=AUX)

    for i in range(len(A)):
        full_adder(circuit=circuit, 
                   a=A[i], 
                   b=B[i], 
                   r=R[i], 
                   c_in=AUX[i % 2], 
                   c_out=AUX[(i+1) % 2], 
                   AUX=AUX[2:])
        
    reset_bits(bits=AUX)

def controlled_add(circuit, control, A, B, R, AUX):
    # Needs len(AUX)=5

    l = len(A)
    reset_bits(bits=AUX)

    for i in range(len(A)):
        controlled_full_adder(circuit=circuit, 
                   control=control,
                   a=A[i], 
                   b=B[i], 
                   r=R[i], 
                   c_in=AUX[i % 2], 
                   c_out=AUX[(i+1) % 2], 
                   AUX=AUX[2:])


def subtract(circuit, A, B, R, AUX):
    """
    Function subtract(circuit,A,B,R,AUX) implements a circuit that subtracts Number(B)
    from Number(A) and stores the result in register R. Assume that len(A) = len(B) = len(R).
    Such a circuit can be obtained by negating each bit stored in B, and by applying the adder
    circuit with the first carry-in bit set to 1 instead of 0 (Figure 9).

    Needs (3 * len(A)) + 5 total qubits
    Needs len(AUX)=5
    """

    l = len(A)

    for i in range(len(B)): # negate all bits of B
        circuit.x(B[i])

    reset_bits(AUX)
    circuit.x(AUX[0]) # Set c_in = 1

    for i in range(l):
        full_adder(circuit=circuit, 
                   a=A[i], 
                   b=B[i], 
                   r=R[i], 
                   c_in=AUX[i % 2], 
                   c_out=AUX[(i+1) % 2], 
                   AUX=AUX[2:])

    for i in range(len(B)): # bring back the bits of B
        circuit.x(B[i])


def controlled_subtract(circuit, control, A, B, R, AUX):
    # Needs len(AUX)=5
    l = len(A)
    
    for i in range(len(B)): # negate all bits of B
        circuit.cx(control, B[i])

    reset_bits(AUX)
    circuit.cx(control, AUX[0]) # Set c_in = 1

    for i in range(l):
        controlled_full_adder(circuit=circuit, 
                   control=control,
                   a=A[i], 
                   b=B[i], 
                   r=R[i], 
                   c_in=AUX[i % 2], 
                   c_out=AUX[(i+1) % 2], 
                   AUX=AUX[2:])

    for i in range(len(B)): # bring back the bits of B
        circuit.cx(control, B[i])

    # we have to copy A to R if control is 0
    circuit.x(control)
    controlled_copy(circuit=circuit, control=control, A=A, B=R)
    circuit.x(control)


def greater_than(circuit, A, B, r, AUX):
    # IDEA:
    # 1) compute B-A
    # 2) if the carry out of the subtraction is 0, then A>B
    #   -> the negation of the carry out is A > B
    #
    #! -> the subtraction function should NOT reset AUX after the computation

    reset_bits(AUX)
    result_register = AUX[:len(A)]
    aux_subtract=AUX[len(A):]

    subtract(circuit=circuit, A=B, B=A, R=result_register, AUX=aux_subtract)

    copy(circuit, [aux_subtract[len(A)%2]], [r])
    circuit.x(r)

    reset_bits(AUX)


def add_mod(circuit, N, A, B, R, AUX):
    # Needs len(AUX) = 2*len(A)+6
    reset_bits(bits=AUX)

    result_add = AUX[:len(A)]
    result_gt = AUX[len(A):len(A)+1]
    add_sub_aux = AUX[len(A)+1:len(A)+1+5]
    gt_aux = AUX[len(A)+1:len(A)+1+5+len(A)]

    add(circuit=circuit, A=A, B=B, R=result_add, AUX=add_sub_aux) # add both numbers
    
    greater_than(circuit=circuit, A=result_add, B=N, r=result_gt, AUX=gt_aux) # test whether the result is greater than N
    
    controlled_subtract(circuit=circuit, control=result_gt, A=result_add, B=N, R=R, AUX=add_sub_aux) # if yes, then subtract N from the result
    
    reset_bits(bits=AUX)


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
