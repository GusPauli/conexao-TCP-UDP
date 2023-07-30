import socket
import os
import sys
import time

namefile = '100MB.txt'
new_file = 'arquivo-recebido_TCP.txt'

# Verifica se foi criado
if os.path.exists(new_file):
    # Se ja existe, deleta
    os.remove(new_file)
else:
    pass

HostServer = '127.0.0.1'
port = 7777
address = (HostServer, port)
pacotes= 0
buffer = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)
print('Conectado\n')

tamanho = int(client.recv(buffer).decode("utf-8"))  # Receber o tamanho do pacote do servidor

client.send(namefile.encode("utf-8"))

start_time = time.time()
with open(new_file, 'wb') as file:
    while True:
    	
        data = client.recv(tamanho)
        #pacotes = pacotes + 1
        if not data:
            break

        file.write(data)
        pacotes = pacotes + 1

end_time = time.time()
final_time = end_time - start_time

print('recebido!\n')
print(f"tamanho dos pacotes: {tamanho}")
print(f"Tamanho do arquivo recebido: {(os.path.getsize(new_file))}")
print(f"Quantidade de pacotes recebidos: {pacotes}")
print(f"Tempo para receber o arquivo: {final_time:.2f} segundos")

client.close()
