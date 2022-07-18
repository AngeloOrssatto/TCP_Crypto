import socket
import tqdm
import time

IP = "localhost"
PORT = 5001

BUFFER_SIZE = 1000
SEPARATOR = "<SEPARATOR>"
BLOCKS = 0
# criando socket do server
# TCP socket
s = socket.socket()

# ligando o socket ao endereço local
s.bind((IP, PORT))
s.listen(5)
print(f"[*] Listening as {IP}:{PORT}")

# se existe conexão, aceita
client_socket, address = s.accept()



# se executar é pq o remetente está conectado
start = time.perf_counter_ns()
print(f"[+] {address} is connected.")

# recebe as informações o arquivo
# recebe usando o socket do client
received = client_socket.recv(BUFFER_SIZE)

BLOCKS += 1
filename, filesize = received.decode('utf-8').split(SEPARATOR)

filename = "teste1.txt"

filesize = int(filesize)

# recebe o arquivo do socket e escreve no arquivo
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # lê 1024 bytes do socket
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            #se não recebe nada é pq já recebeu tudo
            break
        # escreve no arquivo os bytes recebidos
        f.write(bytes_read)
        # print(message_dec)
        BLOCKS += 1
        # atualiza a barra de progresso
        progress.update(len(bytes_read))

# fecha o socket do client e do server
client_socket.close()
s.close()
end = time.perf_counter_ns()
print (f"\nTempo total de transmissão: {end - start}")
print(f"Quantidade de blocos recebidos: {BLOCKS}")