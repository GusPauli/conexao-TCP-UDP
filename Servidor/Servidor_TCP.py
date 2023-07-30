import socket
import os
import sys
import time

namefile = '100MB.txt'
file_size = os.path.getsize(namefile)

host = '127.0.0.1'
port = 7777
address = (host, port)
buffer = 1024
pacotes = 0

# Create the TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
server.listen()

print('Waiting for connection...')

connection, address = server.accept()

print(f"Connection established with client {address} successfully!")

# Packet size options
packet_sizes = {
    '1': 100,
    '2': 500,
    '3': 1000
}

while True:
    print("Choose the packet size:")
    print("1 - 100 bytes")
    print("2 - 500 bytes")
    print("3 - 1000 bytes")
    opcao = input()

    if opcao in packet_sizes:
        tamanho = packet_sizes[opcao]
        break
    else:
        print("Invalid option")

# Send the packet size choice to the client
connection.send(str(tamanho).encode("utf-8"))

# Check if the file exists
if not os.path.exists(namefile):
    print("File not found")
    sys.exit()

# Start the timer to send the file
start_time = time.time()

# Receive the filename from the client
namefile = connection.recv(buffer).decode("utf-8")

with open(namefile, 'rb') as file:
    while True:
        data = file.read(tamanho)
        if not data:
            break

        connection.send(data)
        pacotes += 1

end_time = time.time()

final_time = end_time - start_time

print(f"File Sent! :)\n")
print(f"Packet size chosen: {tamanho} bytes")
print(f"File size sent: {file_size}")
print(f"Quantidade de pacotes mandados: {pacotes}")
print(f"Time taken to send the file: {final_time:.2f} seconds")

connection.close()
server.close()

