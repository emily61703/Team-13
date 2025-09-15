# CURRENTLY A WORK IN PROGRESS, THIS IS ONLY A COPY FROM DR. STROTHER
import socket 

localIP = "0.0.0.0"
localPort = 7501 # needs to match the client port
bufferSize = 1024
messageFromServer = "Hello client"
bytesToSend = str.encode(messageFromServer)

# create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# listen for incoming datagrams
while(True):
    # wait for and recieve message from client
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0] # message
    address = bytesAddressPair[1]   # address 

    # format recieved message and client address
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    # print message and client address to console
    print(clientMsg)
    print(clientIP)

    # send a reply to the client
    UDPServerSocket.sendto(bytesToSend, address)

UDPServerSocket.close()

# INTEGRATION TASKS STILL TO DO:
# - connect UDP broadcast to database updates
# - add network selection to GUI
# - test on multiple devices on same network
