import socket
import json

# Server configuration
localIP = "0.0.0.0"  # Listen on all available interfaces
localPort = 7500
bufferSize = 1024
broadcast_network = "255.255.255.255"  # Default broadcast address

# Create and configure UDP socket for listening
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((localIP, localPort))

# Create separate socket for broadcasting
broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"UDP server listening on {localIP}:{localPort}")
print(f"Broadcasting to network: {broadcast_network}")
print("Type 'network <address>' to change broadcast network")

# Send initial start signal to traffic generator
startSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
startSocket.sendto("202".encode(), ("localhost", 7500))
print("Sent start signal to traffic generator")

def broadcast_equipment(player_data):
    """Broadcast equipment data to all clients on the network"""
    try:
        data = json.dumps(player_data).encode('utf-8')
        broadcastSocket.sendto(data, (broadcast_network, localPort))
        print(f"✓ Broadcasted equipment to network")
        return True
    except Exception as e:
        print(f"Broadcast error: {e}")
        return False

def change_network(new_network):
    """Change the broadcast network address"""
    global broadcast_network
    broadcast_network = new_network
    print(f"Broadcast network changed to: {broadcast_network}")

# Listen for incoming broadcasts
while True:
    try:
        # Receive message and client address
        data, address = serverSocket.recvfrom(bufferSize)
        
        try:
            # Try to decode as JSON first
            message = json.loads(data.decode('utf-8'))
            print(f"\n=== Player Added from {address[0]}:{address[1]} ===")
            print(f"Player ID: {message['player_id']}")
            print(f"Equipment: {message['equipment_code']}")
            print(f"Team: {message['team']}")
            broadcast_equipment(message)
            
        except json.JSONDecodeError:
            # Handle non-JSON messages (from traffic generator)
            message = data.decode('utf-8')
            print(f"Received message from {address}: {message}")
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        break
    except Exception as e:
        print(f"Error: {e}")
        
serverSocket.close()
broadcastSocket.close()