import cirq
import numpy as np
import random
from cryptography.fernet import Fernet

class QRNG():
    def __init__(self, simulator=None):
        if simulator is None:
            simulator = cirq.Simulator()
        self.simulator=simulator
    def generate_binary_array(self, length, showsteps):
        #Initialize Qubit Array
        qubits = cirq.NamedQubit.range(length, prefix="qnum_")
        #Randomization using the Hadamard Gate
        hadamard_gate = [cirq.H(qubit) for qubit in qubits]
        #Measure Results
        measurement_gate = cirq.measure(qubits, key = "qrng_measure")
        #Create circuit
        qrng_circuit = cirq.Circuit(hadamard_gate, measurement_gate)        
        #Show work or not
        simulator = self.simulator
        if showsteps:
            for step, i in enumerate(simulator.simulate_moment_steps(qrng_circuit)):
                print(f'Step: {step}, State:{i.state_vector()}' )
        #Simulate Quantum Env
        result = simulator.simulate(qrng_circuit)
        print(result.measurements['qrng_measure'].tostring())
        return result.measurements['qrng_measure'].tostring()