import socket
import json

# Server configuration
localIP = "0.0.0.0"  # Listen on all available interfaces
localPort = 7501
bufferSize = 1024

# Create and configure UDP socket
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverSocket.bind((localIP, localPort))

print(f"UDP server listening on {localIP}:{localPort}")

# Listen for incoming broadcasts
while True:
    try:
        # Receive message and client address
        data, address = serverSocket.recvfrom(bufferSize)
        
        try:
            # Try to decode JSON message
            message = json.loads(data.decode('utf-8'))
            print(f"\nBroadcast from {address[0]}:{address[1]}")
            print(f"Player: {message['player_id']}")
            print(f"Equipment: {message['equipment_code']}")
            print(f"Team: {message['team']}")
        except json.JSONDecodeError:
            print(f"Received invalid data from {address}")
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
        break
    except Exception as e:
        print(f"Error: {e}")

serverSocket.close()
