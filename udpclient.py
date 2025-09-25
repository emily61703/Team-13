# CURRENTLY A WORK IN PROGRESS, THIS IS ONLY A COPY FROM DR. STROTHER
import socket 
import json 
from datetime import datetime 

class UDPBroadcaster: 
    """Class to handle UDP broadcasting of player equipment information, 
    allows sending messages across a network"""
    
    def __init__(self, port=7501):
        """ Initialize the UDP broadcaster on the specified port """
        self.port = port    # create UDP socket for network communication
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  # UDP protocol
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # enable broadcasting

    """ FUNTIONS """
    def broadcast_player_equipment(self, player_id, equipment_code, team):
       try: # create message dictionary with player info
            message = {
                "type": "new_player",
                "player_id": player_id,
                "equipment": equipment_code,
                "team": team,
                "timestamp": datetime.now().isoformat()
            }
            
            # convert message to JSON and send as bytes
            bytes_to_send = str.encode(json.dumps(message))
            broadcast_address = ("255.255.255.255", self.port)  # broadcast address - sends to all devices 
            self.socket.sendto(bytes_to_send, broadcast_address) # send message
            return True
       except Exception as e:
            print(f"Broadcast error: {e}")
            return False

    def close(self):
        """ Close the UDP socket when done"""
        self.socket.close()