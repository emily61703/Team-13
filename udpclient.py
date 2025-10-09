import socket
import json

# Client configuration
serverPort = 7501
bufferSize = 1024
network = "255.255.255.255"  # Default broadcast address

# Create and configure UDP socket
clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def broadcast_equipment(player_id, equipment_code, team, network_addr=network):
    """Broadcast player equipment data"""
    message = {
        "player_id": player_id,
        "equipment_code": equipment_code,
        "team": team
    }
    
    try:
        # Convert message to JSON and encode
        data = json.dumps(message).encode('utf-8')
        # Send broadcast
        clientSocket.sendto(data, (network_addr, serverPort))
        return True
    except Exception as e:
        print(f"Broadcast error: {e}")
        return False

def change_network(new_network):
    """Change broadcast network address"""
    global network
    network = new_network

# Clean up when done
def cleanup():
    clientSocket.close()
