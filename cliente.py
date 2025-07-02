import socket as sock
import threading
import tkinter as tk
from tkinter import scrolledtext

# IP e PORTA do servidor
HOST = '127.0.0.1'
PORTA = 9999
socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Cliente solicita conexão
socket_cliente.connect((HOST, PORTA))

# Função para receber mensagens do servidor
def recebe_mensagens():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            if mensagem:
                chat_text_area.config(state='normal')
                chat_text_area.insert(tk.END, mensagem + '\n')
                chat_text_area.config(state='disabled')
                chat_text_area.yview(tk.END)
        except:
            print("Erro ao receber a mensagem... Desconectado.")
            socket_cliente.close()
            break

# Função para enviar mensagem
def enviar_mensagem():
    mensagem = msg_entry.get()
    if mensagem:
        socket_cliente.sendall(mensagem.encode())
        msg_entry.delete(0, tk.END)

# Interface gráfica com Tkinter
def iniciar_interface():
    global chat_text_area, msg_entry

    root = tk.Tk()
    root.title("Chat Cliente")

    # Área de texto para o chat
    chat_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
    chat_text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Entrada para mensagens
    msg_entry = tk.Entry(root, width=80)
    msg_entry.pack(side=tk.LEFT, padx=10, pady=5)
    msg_entry.bind("<Return>", lambda event: enviar_mensagem())

    # Botão para enviar mensagens
    enviar_btn = tk.Button(root, text="Enviar", command=enviar_mensagem)
    enviar_btn.pack(side=tk.RIGHT, padx=10, pady=5)

    # Iniciar thread para receber mensagens
    thread_receber = threading.Thread(target=recebe_mensagens)
    thread_receber.daemon = True
    thread_receber.start()

    root.mainloop()

# Solicitar nome do usuário e enviar para o servidor
nome = input("Informe seu nome para entrar no chat: ")
socket_cliente.sendall(nome.encode())

# Iniciar a interface gráfica
iniciar_interface()
