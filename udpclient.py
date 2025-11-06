import socket
import json

# Client configuration
SERVER_PORT = 7500  # Changed from 7501
BROADCAST_ADDR = "255.255.255.255"
BUFFER_SIZE = 1024

# Create and configure UDP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def broadcast_equipment(player_id, equipment_code, team):
    """Broadcast player equipment data"""
    message = {
        "player_id": player_id,
        "equipment_code": equipment_code,
        "team": team
    }
    
    try:
        data = json.dumps(message).encode('utf-8')
        clientSocket.sendto(data, (BROADCAST_ADDR, SERVER_PORT))
        print(f"Broadcast sent: {message}")
        return True
    except Exception as e:
        print(f"Broadcast error: {e}")
        return False

def cleanup():
    """Close socket when done"""
    clientSocket.close()