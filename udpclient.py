# CURRENTLY A WORK IN PROGRESS, THIS IS ONLY A COPY FROM DR. STROTHER
import socket 

messageFromClient = "Hello server"  # this is the message to be sent to the server side
bytesToSend = str.encode(messageFromClient) # udp requires bytes, this encodes the string to bytes

# defining server connection parameters
serverAddressPort = ("127.0.0.1", 7501)
bufferSize = 1024   # max size of message to be received at once

# creating a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# enable broadcast option
# this allows sending messages to all devices on the network
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# wait for and recieve reponse from server 
messageFromServer = UDPClientSocket.recvfrom(bufferSize)
message = messageFromServer[0]

print(message)

UDPClientSocket.close()

# INTEGRATION TASKS STILL TO DO:
# - connect UDP broadcast to database updates
# - add network selection to GUI
# - test on multiple devices on same network