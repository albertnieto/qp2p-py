import random
from typing import Any, Dict
from loguru import logger
from .base import QuantumProtocol

class BB84(QuantumProtocol):
    def generate_qubits(self, num_qubits: int) -> Dict[str, Any]:
        logger.info(f"Generating {num_qubits} qubits...")
        bases = [random.choice(['+', '×']) for _ in range(num_qubits)]
        bits = [random.randint(0, 1) for _ in range(num_qubits)]
        logger.info(f"Bases generated: {bases}")
        logger.info(f"Bits generated: {bits}")
        return {'bases': bases, 'bits': bits}

    def measure_qubits(self, qubits_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Measuring qubits with data: {qubits_data}")
        my_bases = [random.choice(['+', '×']) for _ in range(len(qubits_data['bases']))]
        measured_bits = []
        for i in range(len(my_bases)):
            if my_bases[i] == qubits_data['bases'][i]:
                measured_bits.append(qubits_data['bits'][i])
            else:
                measured_bits.append(random.randint(0, 1))
        logger.info(f"My bases: {my_bases}")
        logger.info(f"Measured bits: {measured_bits}")
        return {'bases': my_bases, 'bits': measured_bits}

    def reconcile(self, alice_data, bob_data):
        logger.info(f"Reconciling Alice data: {alice_data} with Bob data: {bob_data}")
        matching_bases = [i for i in range(len(alice_data['bases'])) 
                          if alice_data['bases'][i] == bob_data['bases'][i]]
        logger.info(f"Matching bases indices: {matching_bases}")
        raw_key = [alice_data['bits'][i] for i in matching_bases]
        logger.info(f"Raw key: {raw_key}")
        return raw_key
