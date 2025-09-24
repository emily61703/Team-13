import socket
import json
import sqlite3

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
            
            #Save to the Database
            save_player_data(message['player_id'], message['equipment'], 
                message['team'], message['timestamp'])
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
    
    # Initializing Database
    init_database()
    print("Database initialized")

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

def init_database():
    """Create a simple database to store player equipment data"""
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT,
            equipment_code TEXT,
            team TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_player_data(player_id, equipment, team, timestamp):
    """Save received player data to database"""
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO player_equipment (player_id, equipment_code, team, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (player_id, equipment, team, timestamp))
    
    conn.commit()
    conn.close()
    print(f"Player {player_id} data saved to database")
