import socket
import json

# Server Configuration
localIP = "0.0.0.0"  # Listen on all available network interfaces
localPort = 7501     # Port number - must match client's port
bufferSize = 1024    # Maximum size of received message in bytes

# Initialize response message
messageFromServer = "Player equipment received"  # Acknowledgment message
bytesToSend = str.encode(messageFromServer)     # Convert to bytes for transmission

def handle_player_message(message_bytes):
    """
    Process received player equipment messages
    """
    try:
        # Decode JSON message from bytes
        message = json.loads(message_bytes.decode())
        
        if message["type"] == "new_player":
            # Extract and display player information
            print("\nNew Player Equipment Broadcast Received:")
            print(f"Player ID: {message['player_id']}")
            print(f"Equipment Code: {message['equipment']}")
            print(f"Team: {message['team']}")
            print(f"Timestamp: {message['timestamp']}")
            return True
    except json.JSONDecodeError:
        print("Error: Invalid JSON message format")
    except KeyError:
        print("Error: Missing required fields in message")
    except Exception as e:
        print(f"Error processing message: {e}")
    return False

# Create UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

try:
    # Bind socket to address and port
    UDPServerSocket.bind((localIP, localPort))
    print(f"UDP server listening on port {localPort}")

    # Main server loop
    while True:
        try:
            # Wait for and receive incoming datagram
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]    # Message content
            address = bytesAddressPair[1]    # Sender's address (IP, port)

            # Process the received message
            if handle_player_message(message):
                # Send acknowledgment back to client
                UDPServerSocket.sendto(bytesToSend, address)
                print(f"Acknowledgment sent to {address}")

        except socket.error as e:
            print(f"Socket error occurred: {e}")
            continue

except KeyboardInterrupt:
    print("\nServer shutdown requested")
except Exception as e:
    print(f"Server error: {e}")
finally:
    # Clean up resources
    UDPServerSocket.close()
    print("Server shut down")

# INTEGRATION TASKS STILL TO DO:
# - connect UDP broadcast to database updates (done)
# - add network selection to GUI
# - test on multiple devices on same network
