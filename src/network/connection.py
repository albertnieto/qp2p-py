import socket
import threading
import json
from loguru import logger

class QuantumChannel:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = []
        self.running = False
        self.logger = logger

    def start_server(self):
        self.running = True
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        threading.Thread(target=self._accept_connections, daemon=True).start()

    def _accept_connections(self):
        while self.running:
            try:
                conn, addr = self.sock.accept()
                self.connections.append(conn)
                self.logger.info(f"Quantum connection from {addr}")
            except:
                break

    def connect(self, host, port):
        self.sock.connect((host, port))
        self.connections.append(self.sock)

    def send(self, data):
        try:
            serialized = json.dumps(data).encode()
            for conn in self.connections:
                conn.sendall(serialized + b'\n')
        except Exception as e:
            self.logger.error(f"Send error: {e}")

    def receive(self):
        try:
            data = self.sock.recv(4096).decode().strip()
            return json.loads(data)
        except:
            return None

    def stop(self):
        self.running = False
        self.sock.close()

class ClassicalChannel(QuantumChannel):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.logger = logger
