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

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(address)

print('Waiting for connection...')

# Receber o nome do arquivo do cliente
data, client_address = server.recvfrom(buffer)
namefile = data.decode("utf-8")

while True:
    print("Choose the packet size:")
    print("1 - 100 bytes")
    print("2 - 500 bytes")
    print("3 - 1000 bytes")
    opcao = input()

    if opcao == '1':
        tamanho = 100
        break
    elif opcao == '2':
        tamanho = 500
        break
    elif opcao == '3':
        tamanho = 1000
        break
    else:
        print("Invalid option")

# Enviar o tamanho do pacote escolhido ao cliente
server.sendto(str(tamanho).encode("utf-8"), client_address)

# Verificar se o arquivo existe
if not os.path.exists(namefile):
    print("File not found")
    sys.exit()

# Começar a contagem de tempo para enviar o arquivo
start_time = time.time()

with open(namefile, 'rb') as file:
    while True:
        data = file.read(tamanho)
        if not data:
            break

        server.sendto(data, client_address)
        pacotes = pacotes + 1

end_time = time.time()
final_time = end_time - start_time

print(f"File sent! :)\n")
print(f"Packet size chosen: {tamanho} bytes")
print(f"File size sent: {file_size}")
print(f"Quantidade de pacotes mandados: {pacotes}")
print(f"Time taken to send the file: {final_time:.2f} seconds")

server.close()
