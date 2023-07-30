import socket
import os
import sys
import time

namefile = '100MB.txt'
new_file = 'arquivo-recebido.txt'

# Verificar se o arquivo já existe
if os.path.exists(new_file):
    # Se já existe, deleta
    os.remove(new_file)

host = '127.0.0.1'
port = 7777
address = (host, port)
buffer = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)  # Definir um tempo limite de 5 segundos para a recepção dos pacotes

start_time = time.time()

client.sendto(namefile.encode("utf-8"), address)

# Receber o tamanho do pacote do servidor
data, _ = client.recvfrom(buffer)
tamanho = int(data.decode("utf-8"))

contador = 0 

with open(new_file, 'wb') as file:
    while True:
        try:
            data, _ = client.recvfrom(buffer)
            
            if data == b'EOF':
                break

            file.write(data)
            contador += 1

            # Enviar confirmação ao servidor
            client.sendto(str(contador).encode("utf-8"), address)
            
        except socket.timeout:
            # Tempo limite atingido, reenviar a última confirmação
            client.sendto(str(contador).encode("utf-8"), address)

end_time = time.time()
final_time = end_time - start_time

print('Received!\n')
print(f"Tamanho do arquivo recebido: {os.path.getsize(new_file)}")
print(f"Quantidade de pacotes recebidos: {contador}")
print(f"Tempo para receber o arquivo: {final_time:.2f} segundos")

client.close()

