import hashlib
from loguru import logger
from typing import List
from threading import Lock
from ..protocols.bb84 import BB84
from .connection import QuantumChannel, ClassicalChannel

class Node:
    def __init__(self, host: str = 'localhost', q_port: int = 5000, c_port: int = 5001):
        self.host = host
        self.q_port = q_port
        self.c_port = c_port
        self.quantum_channel = QuantumChannel(host, q_port)
        self.classical_channel = ClassicalChannel(host, c_port)
        self.protocol = BB84()
        self.keys = {}
        self.lock = Lock()
        self.peers = []
        self.logger = logger

    def start(self):
        self.quantum_channel.start_server()
        self.classical_channel.start_server()
        self.logger.info(f"Node started on {self.host}:{self.q_port} (quantum) {self.c_port} (classical)")

    def connect_to_peer(self, peer_host, peer_q_port, peer_c_port):
        try:
            # Connect quantum channel
            q_conn = QuantumChannel(self.host, self.q_port)
            q_conn.connect(peer_host, peer_q_port)
            
            # Connect classical channel
            c_conn = ClassicalChannel(self.host, self.c_port)
            c_conn.connect(peer_host, peer_c_port)
            
            self.peers.append({
                'host': peer_host,
                'quantum': q_conn,
                'classical': c_conn
            })
            self.logger.info(f"Connected to {peer_host}:{peer_q_port}")
            return True
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            return False

    def perform_handshake(self, peer):
        # Exchange basis information and reconcile keys
        alice_data = self.protocol.generate_qubits(256)
        peer['quantum'].send(alice_data)
        
        bob_data = peer['quantum'].receive()
        measured_data = self.protocol.measure_qubits(bob_data)
        peer['classical'].send(measured_data['bases'])
        
        alice_bases = peer['classical'].receive()
        raw_key = self.protocol.reconcile(
            {'bases': alice_data['bases'], 'bits': alice_data['bits']},
            {'bases': alice_bases, 'bits': measured_data['bits']}
        )
        
        # Privacy amplification
        final_key = hashlib.sha256(bytes(raw_key)).digest()
        with self.lock:
            self.keys[peer['host']] = final_key
        self.logger.info(f"Established key with {peer['host']}")

    def initiate_key_exchange(self, peer_host, peer_q_port, peer_c_port):
        if self.connect_to_peer(peer_host, peer_q_port, peer_c_port):
            peer = self.peers[-1]
            self.perform_handshake(peer)

    def stop(self):
        self.quantum_channel.stop()
        self.classical_channel.stop()
