from loguru import logger
import threading
import time
from src.network.node import Node

def run_node(node, peers):
    node.start()
    time.sleep(1)
    for peer in peers:
        node.initiate_key_exchange(peer['host'], peer['q_port'], peer['c_port'])
    while True:
        time.sleep(1)

if __name__ == "__main__":
    
    # Node configuration
    nodes = [
        {'host': 'localhost', 'q_port': 5000, 'c_port': 5001},
        {'host': 'localhost', 'q_port': 5002, 'c_port': 5003},
        {'host': 'localhost', 'q_port': 5004, 'c_port': 5005}
    ]

    # Start all nodes
    threads = []
    for i, config in enumerate(nodes):
        node = Node(config['host'], config['q_port'], config['c_port'])
        peers = [n for n in nodes if n != config]
        t = threading.Thread(target=run_node, args=(node, peers))
        t.start()
        threads.append(t)
        time.sleep(0.5)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down nodes...")
        for t in threads:
            t.join()