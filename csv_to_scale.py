import csv
import socket

# IP address and port of the remote device
ip_address = "10.6.1.250"
port = 5002

# Read PLU data from CSV file
plu_data = []
with open('C:/Users/myagmardorj/Git/lesson3/file06.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        plu_data.append(';'.join(row))  # Assuming each row is a CSV string

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((ip_address, port))
    client_socket.settimeout(4)
    # Send PLU data to the server
    for plu_entry in plu_data:
        client_socket.sendall(plu_entry.encode('utf-8'))
        client_socket.sendall('\n'.encode('utf-8'))  # Assuming each entry is terminated by a newline character
        
    print("PLU data sent successfully.")

except Exception as e:
    print("Error:", e)

finally:
    # Close the socket connection
    client_socket.close()
