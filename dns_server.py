import socket # Import the socket module for creating a socket and sending/receiving data over a network
import sqlite3 # Import the sqlite3 module for interacting with a SQLite database

# Define the DNS server's IP address and port
DNS_SERVER_IP = '10.10.10.1' # IP address of the DNS server
DNS_SERVER_PORT = 12345 # Port number for the DNS server

# Create a connection to the DNS database
conn = sqlite3.connect('dns.db') # Connect to the database file named "dns.db"
cursor = conn.cursor() # Create a cursor object for interacting with the database

# Create the DNS table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS dns
                (domain text PRIMARY KEY, ip_address text)''') # Create a table named "dns" with columns "domain" and "ip_address"
conn.commit() # Save the changes to the database

# Print a message indicating that the DNS server is listening
print('DNS server listening on {}:{}'.format(DNS_SERVER_IP, DNS_SERVER_PORT))

# Create a UDP socket and bind it to the DNS server's IP address and port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket
sock.bind((DNS_SERVER_IP, DNS_SERVER_PORT)) # Bind the socket to the DNS server's IP address and port

while True: # Keep the server running indefinitely
    try:
        # Receive a DNS query packet from a client
        data, addr = sock.recvfrom(1024) # Receive data from the socket and get the address of the client that sent the data

        # Decode the DNS query packet
        domain = data.decode().strip() # Convert the data to a string and remove any leading/trailing whitespace

        # Look up the IP address for the requested domain in the DNS database
        cursor.execute("SELECT ip_address FROM dns WHERE domain=?", (domain,)) # Execute a SQL query to get the IP address for the requested domain
        result = cursor.fetchone() # Get the first row of the query result
        if result:
            ip_address = result[0] # Get the IP address from the query result
        else:
            ip_address = '0.0.0.0' # Use a default IP address if the domain wasn't found in the database

        # Encode the IP address as a DNS response packet and send it back to the client
        response = ip_address.encode() # Convert the IP address to bytes
        sock.sendto(response, addr) # Send the bytes back to the client
    except Exception as e: # Handle any errors that occur while processing the request
        print('Error:', e)

    conn.close() # Close the database connection when the server is stopped
