from gates import *
from utilities import *

def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    """
    Function full_adder(circuit,a,b,r,c_in,c_out,AUX) implements a full adder (Figure
    3). The registers a and b store the bits to be added, c_in stores the carry-in bit, c_out
    stores the carry-out bit, r stores the result of the sum, and AUX is the auxiliary register.

    Needs len(AUX)=3.
    """
    reset_bits(circuit=circuit, bits=AUX)
    circuit.reset(c_out) # !! c_out must be 0 at the beginning
    
    xor_gate(circuit=circuit, a=a, b=b, output=AUX[0])
    xor_gate(circuit=circuit, a=AUX[0], b=c_in, output=r)

    and_gate(circuit=circuit, a=a, b=b, output=AUX[1])
    and_gate(circuit=circuit, a=AUX[0], b=c_in, output=AUX[2])

    or_gate(circuit=circuit, a=AUX[1], b=AUX[2], output=c_out)

    reset_bits(circuit=circuit, bits=AUX)


def controlled_full_adder(circuit, control, a, b, r, c_in, c_out, AUX):
    reset_bits(circuit=circuit, bits=AUX)
    circuit.reset(c_out) # !! c_out must be 0 at the beginning
    
    controlled_xor_gate(circuit=circuit, c=control, a=a, b=b, output=AUX[0])
    controlled_xor_gate(circuit=circuit, c=control, a=AUX[0], b=c_in, output=r)

    controlled_and_gate(circuit=circuit, c=control, a=a, b=b, output=AUX[1])
    controlled_and_gate(circuit=circuit, c=control, a=AUX[0], b=c_in, output=AUX[2])

    controlled_or_gate(circuit=circuit, c=control, a=AUX[1], b=AUX[2], output=c_out)

    reset_bits(circuit=circuit, bits=AUX)


def add(circuit, A, B, R, AUX):
    # Needs len(AUX)=5

    l = len(A)
    reset_bits(circuit=circuit, bits=AUX)

    for i in range(len(A)):
        full_adder(circuit=circuit, 
                   a=A[i], 
                   b=B[i], 
                   r=R[i], 
                   c_in=AUX[i % 2], 
                   c_out=AUX[(i+1) % 2], 
                   AUX=AUX[2:])
        
    reset_bits(circuit=circuit, bits=AUX)

def controlled_add(circuit, control, A, B, R, AUX):
    # Needs len(AUX)=5

    l = len(A)
    reset_bits(circuit=circuit, bits=AUX)

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

    reset_bits(circuit, AUX)
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

    reset_bits(circuit, AUX)
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

    reset_bits(circuit, AUX)
    result_register = AUX[:len(A)]
    aux_subtract=AUX[len(A):]

    subtract(circuit=circuit, A=B, B=A, R=result_register, AUX=aux_subtract)

    copy(circuit, [aux_subtract[len(A)%2]], [r])
    circuit.x(r)

    reset_bits(circuit, AUX)


def add_mod(circuit, N, A, B, R, AUX):
    # Needs len(AUX) = 2*len(A)+6
    reset_bits(circuit=circuit, bits=AUX)

    result_add = AUX[:len(A)]
    result_gt = AUX[len(A):len(A)+1]
    add_sub_aux = AUX[len(A)+1:len(A)+1+5]
    gt_aux = AUX[len(A)+1:len(A)+1+5+len(A)]

    add(circuit=circuit, A=A, B=B, R=result_add, AUX=add_sub_aux) # add both numbers
    
    greater_than(circuit=circuit, A=result_add, B=N, r=result_gt, AUX=gt_aux) # test whether the result is greater than N
    
    controlled_subtract(circuit=circuit, control=result_gt, A=result_add, B=N, R=R, AUX=add_sub_aux) # if yes, then subtract N from the result
    
    reset_bits(circuit=circuit, bits=AUX)

def times_two_mod(circuit, N, A, R, AUX):
    # Needs len(AUX) = 3*len(A)+6
    reset_bits(circuit, AUX)

    temp_register = AUX[:len(A)]
    add_mod_aux = AUX[len(A):]

    # Copy A to the temporary register
    copy(circuit, A, temp_register)

    # Compute A + A mod N
    add_mod(circuit=circuit, N=N, A=A, B=temp_register, R=R, AUX=add_mod_aux)

    reset_bits(circuit, AUX)