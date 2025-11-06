# udpclient.py: Handles all outgoing UDP communication

import socket
import json

# Configuration
TRAFFIC_GEN_PORT = 7500
BROADCAST_PORT = 7500
BROADCAST_ADDR = "255.255.255.255"
BUFFER_SIZE = 1024

# Create sockets
acknowledgment_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def send_game_start():
    """Send game start signal (202) to traffic generator"""
    try:
        acknowledgment_socket.sendto("202".encode('utf-8'), ("127.0.0.1", TRAFFIC_GEN_PORT))
        return True
    except Exception as e:
        print(f"Failed to send game start: {e}")
        return False


def send_acknowledgment(address, ack_code="200"):
    """Send acknowledgment to traffic generator"""
    try:
        acknowledgment_socket.sendto(ack_code.encode('utf-8'), address)
        return True
    except Exception as e:
        print(f"Failed to send acknowledgment: {e}")
        return False


def broadcast_equipment(player_id, equipment_code, team):
    """Broadcast player equipment data to network"""
    message = {
        "player_id": player_id,
        "equipment_code": equipment_code,
        "team": team
    }

    try:
        data = json.dumps(message).encode('utf-8')
        broadcast_socket.sendto(data, (BROADCAST_ADDR, BROADCAST_PORT))
        print(f"Broadcast sent: {message}")
        return True
    except Exception as e:
        print(f"Broadcast error: {e}")
        return False


def cleanup():
    """Close all sockets"""
    acknowledgment_socket.close()
    broadcast_socket.close()