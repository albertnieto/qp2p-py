from abc import ABC, abstractmethod
from typing import Dict, Any

class QuantumProtocol(ABC):
    @abstractmethod
    def generate_qubits(self, num_qubits: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def measure_qubits(self, qubits_data: Dict[str, Any]) -> Dict[str, Any]:
        pass