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