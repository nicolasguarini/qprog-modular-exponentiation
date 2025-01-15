from gates import *
from utilities import *

def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    """
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
        
     # we have to copy A to R if control is 0
    circuit.x(control)
    controlled_copy(circuit=circuit, control=control, A=A, B=R)
    circuit.x(control)

    reset_bits(circuit=circuit, bits=AUX)


def subtract(circuit, A, B, R, AUX):
    """
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
    # Needs len(AUX) = 5+len(A)

    reset_bits(circuit, AUX)
    result_register = AUX[:len(A)]
    aux_subtract=AUX[len(A):]

    subtract(circuit=circuit, A=B, B=A, R=result_register, AUX=aux_subtract)

    copy(circuit, [aux_subtract[len(A)%2]], [r])
    circuit.x(r)

    reset_bits(circuit, AUX)


def greater_than_or_equal(circuit, A, B, r, AUX):
    # IDEA:
    # 1) Compute A - B
    # 2) If the carry-out of the subtraction is 1, then A >= B
    #
    #! -> The subtraction function should NOT reset AUX after the computation
    # Needs len(AUX) = 5+len(A)

    reset_bits(circuit, AUX)
    result_register = AUX[:len(A)]
    aux_subtract = AUX[len(A):]

    subtract(circuit=circuit, A=A, B=B, R=result_register, AUX=aux_subtract)

    # Copy the carry-out directly into r (without negation)
    copy(circuit, [aux_subtract[len(A) % 2]], [r])

    reset_bits(circuit, AUX)


def add_mod(circuit, N, A, B, R, AUX):
    # Needs len(AUX) = 2*len(A)+6
    reset_bits(circuit=circuit, bits=AUX)

    result_add = AUX[:len(A)]
    result_gt = AUX[len(A):len(A)+1]
    add_sub_aux = AUX[len(A)+1:len(A)+1+5]
    gt_aux = AUX[len(A)+1:len(A)+1+5+len(A)]

    add(circuit=circuit, A=A, B=B, R=result_add, AUX=add_sub_aux) # add both numbers
    
    greater_than_or_equal(circuit=circuit, A=result_add, B=N, r=result_gt, AUX=gt_aux) # test whether the result is greater than N
    
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


def times_two_power_mod(circuit,N,A,k,R,AUX):
    # Needs len(AUX) = 4*len(A)+6
    reset_bits(circuit=circuit, bits=AUX)

    temp_register = AUX[:len(A)]
    times_two_mod_aux = AUX[len(A):]
    copy(circuit, A, temp_register)

    for i in range(k):
        times_two_mod(circuit=circuit, N=N, A=temp_register, R=R, AUX=times_two_mod_aux)
        reset_bits(circuit=circuit, bits=temp_register) # the copy() function expects B to be |0>
        copy(circuit=circuit, A=R, B=temp_register)
        reset_bits(circuit=circuit, bits=R) # R should never contain intermediate results

    if k > 0:
        copy(circuit=circuit, A=temp_register, B=R)
    else:
        # if k==0, the result will be A mod N
        reset_bits(circuit=circuit, bits=AUX)
        greater_than_or_equal(circuit=circuit, A=A, B=N, r=AUX[0], AUX=AUX[1:])
        controlled_subtract(circuit=circuit, control=AUX[0], A=A, B=N, R=R, AUX=AUX[1:])

    reset_bits(circuit=circuit, bits=AUX)


def multiply_mod(circuit, N, A, B, R, AUX):
    # Needs len(AUX) = 6 * len(A) + 6
    reset_bits(circuit=circuit, bits=AUX)

    temp_register = AUX[:len(A)]
    sum_register = AUX[len(A):2*len(A)]
    times_two_power_mod_aux = AUX[2*len(A):]

    for k in range(len(B)):
        reset_bits(circuit=circuit, bits=temp_register)
        reset_bits(circuit=circuit, bits=R) # controlled_add expects R to be |0>

        times_two_power_mod(circuit=circuit, N=N, A=A, k=k, R=temp_register, AUX=times_two_power_mod_aux) # compute A*2^k mod N

        controlled_add(circuit=circuit, control=B[k], A=sum_register, B=temp_register, R=R, AUX=times_two_power_mod_aux) # sum the result if B[k] == 1

        controlled_copy(circuit, control=B[k], A=R, B=sum_register) # copy sum for next iteration
        
    reset_bits(circuit=circuit, bits=AUX)