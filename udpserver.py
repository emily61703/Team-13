# udpserver.py: Handles all incoming UDP communication

import socket
import threading

# Configuration
LISTEN_PORT = 7501
BUFFER_SIZE = 1024

class UDPServer:
    def __init__(self):
        self.socket = None
        self.running = False
        self.thread = None
        self.callback = None

    def start(self, callback):
        """Start UDP server with callback for incoming messages"""
        if self.running:
            return

        self.callback = callback
        self.running = True

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("0.0.0.0", LISTEN_PORT))
            self.socket.settimeout(1.0)

            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()

            return True
        except Exception as e:
            print(f"Failed to start UDP server: {e}")
            self.running = False
            return False

    def _listen(self):
        """Internal listening loop"""
        while self.running:
            try:
                data, address = self.socket.recvfrom(BUFFER_SIZE)
                decoded = data.decode('utf-8').strip()

                if self.callback:
                    self.callback(decoded, address)

            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"UDP receive error: {e}")

    def stop(self):
        """Stop the UDP server"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        if self.socket:
            self.socket.close()
        self.thread = None
        self.socket = None


# Global server instance
udp_server = UDPServer()