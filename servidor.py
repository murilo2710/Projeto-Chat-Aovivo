import socket as sock
import threading

# Função para envio de mensagens para todos os clientes (broadcast)
def broadcast(mensagem, remetente=None):
    for cliente in lista_clientes:
        if cliente != remetente:
            try:
                cliente[0].sendall(mensagem.encode())
            except:
                remover(cliente)

# Função para envio de mensagens privadas (unicast)
def unicast(mensagem, remetente_socket, destinatario_nome, remetente_nome):
    for cliente in lista_clientes:
        if cliente[1] == destinatario_nome:
            try:
                cliente[0].sendall(f"[Privado] {remetente_nome} >> {mensagem}".encode())
                remetente_socket.sendall(f"[Privado para {destinatario_nome}] {mensagem}".encode())
                return
            except:
                remover(cliente)
    remetente_socket.sendall(f"Usuário {destinatario_nome} não encontrado.".encode())

# Função para remoção de clientes da lista
def remover(cliente):
    if cliente in lista_clientes:
        lista_clientes.remove(cliente)
        broadcast(f"{cliente[1]} saiu do chat.")
        atualizar_lista_conectados()

# Função para atualizar e enviar a lista de clientes conectados a todos os clientes
def atualizar_lista_conectados():
    clientes_conectados = "Usuários conectados: " + ", ".join([cliente[1] for cliente in lista_clientes])
    for cliente in lista_clientes:
        try:
            cliente[0].sendall(clientes_conectados.encode())
        except:
            remover(cliente)

# Função para recebimento de dados dos clientes
def recebe_dados(sock_cliente, endereco):
    # Receber o nome do cliente
    nome = sock_cliente.recv(50).decode()
    lista_clientes.append((sock_cliente, nome))
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco}")
    
    # Notificar todos sobre o novo cliente e atualizar lista de conectados
    broadcast(f"{nome} entrou no chat.")
    atualizar_lista_conectados()
    
    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()
            if mensagem.startswith("@"):
                destinatario, mensagem_privada = mensagem[1:].split(' ', 1)
                unicast(mensagem_privada, sock_cliente, destinatario, nome)
            else:
                broadcast(f"{nome} >> {mensagem}", sock_cliente)
        except:
            print(f"{nome} foi desconectado.")
            remover((sock_cliente, nome))
            sock_cliente.close()
            return

# Configuração do servidor
HOST = '127.0.0.1'
PORTA = 9999
lista_clientes = []
sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_server.bind((HOST, PORTA))
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

# Loop principal do servidor para aceitar conexões
while True:
    sock_conn, ender = sock_server.accept()
    thread_cliente = threading.Thread(target=recebe_dados, args=[sock_conn, ender])
    thread_cliente.start()
