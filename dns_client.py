# Import the socket module
from socket import *

# Specify the server's port and IP address
port = 53
ip = '127.0.0.1'

# Create a UDP socket object
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Enter an infinite loop to allow the user to enter multiple DNS queries
while True:
    # Get a DNS query from the user
    query = input("Enter DNS query: ")

    # Send the query to the server using the sendto() method of the socket object
    clientSocket.sendto(query.encode(), (ip, port))

    # Receive the response from the server using the recvfrom() method of the socket object
    response, address = clientSocket.recvfrom(2048)

    # Print the response
    print(response.decode())

# Close the socket connection
clientSocket.close()
