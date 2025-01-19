def reset_bits(circuit, bits):
    for i in bits:
        circuit.reset(i)


def set_bits(circuit, A, X):
    for i in range(len(X)):
        if X[i] == '1':
            circuit.x(A[i])


def copy(circuit, A, B):
    for i in range(len(A)):
        circuit.cx(A[i], B[i])
    circuit.barrier()

def controlled_copy(circuit, control, A, B):
    for i in range(len(A)):
        circuit.ccx(control, A[i], B[i])


def invert_string(X):
    return "".join([str(int(x)^1) for x in X])
