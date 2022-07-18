import socket
import tqdm
import os
from Crypto.Cipher import AES

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1000

#Endereço ip e porta do server
HOST = "localhost"
PORT = 5001

# arquivo a se enviado
FILENAME = "teste.txt"

# tamanho do arquivo
FILESIZE = os.path.getsize(FILENAME)
BLOCKS = 0

# criando o socket do client
s = socket.socket()

print(f"[+] Connecting to {HOST}:{PORT}")
s.connect((HOST, PORT))
print("[+] Connected.")

KEY = s.recv(BUFFER_SIZE)
#print(f"KEY {bytes_read}")

IV = b"abcdefghijklmnop"
#Objeto para encriptação
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)
#Objeto para decriptação
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)

# enviando o nome do arquivo e o tamanho
message = f"{FILENAME}{SEPARATOR}{FILESIZE}"
message_enc = obj_enc.encrypt(message.encode('utf-8'))
s.send(message_enc)
BLOCKS += 1

# enviando o arquivo
progress = tqdm.tqdm(range(FILESIZE), f"Sending {FILENAME}", unit="B", unit_scale=True, unit_divisor=1024)
with open(FILENAME, "rb") as f:
    while True:
        # lendo bytes do arquivo
        bytes_read = f.read(BUFFER_SIZE)
        message_enc = obj_enc.encrypt(bytes_read)
        if not bytes_read:
            # se acabou de transmitir os bytes do arquivo
            break
        # sendall para garantir a transmissão
        s.sendall(message_enc)
        BLOCKS += 1
        # atualização da barra de progresso
        progress.update(len(bytes_read))
# fecha o socket
s.close()
print(f"Quantidade de blocos enviados: {BLOCKS}")