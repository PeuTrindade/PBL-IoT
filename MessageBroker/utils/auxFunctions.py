import socket
import pickle
import json
import threading

tcpPort = 4000
udpPort = 5000
tcpServer = None
udpServer = None

# Dicionário para armazenar os dispositivos conectados.
connectedDevices = {}
# Dicionário para armazenar os objetos de conexões de cada dispositivo conectado.
connections = {}

# Função responsável por salvar uma conexão ao dicionário de conexões.
def save_device(connection, address):
    global connectedDevices
    
    connection.sendto(str("Dispositivo conectado o broker com sucesso!").encode(), (address[0], tcpPort))
    connectedDevices[address[1]] = {"addressInfo": address, "sentMessages": {}}
    connections[str(address[1])] = connection
        
    print(f"Um novo dispositivo foi conectado: {address[1]}")

# Função responsável por enviar o modo escolhido em TCP ao dispositivo.
def change_device_mode(port, mode):
    try:
        connections[str(port)].sendall(str(mode).encode())
    except e:
        print(e)

# Função responsável por enviar a temperatura escolhida em TCP ao dispositivo.      
def change_device_temperature(port, temperature):
    try:
        connections[str(port)].sendall(str(temperature).encode())
    except e:
        print(e)

# Função responsável por receber as mensagens UDP e salvar no dicionário.
def receive_udp_message(udpServer):
    global connectedDevices
    
    message, address = udpServer.recvfrom(4096)
    
    decoded_message = json.loads(message.decode())
    
    message_tcp_port = decoded_message['tcpServerPort']
    
    if message_tcp_port in connectedDevices:
        # Caso o dispositivo esteja inativo, suas informações são removidas do dicionário.
        if decoded_message['on'] == None:
            connectedDevices.pop(message_tcp_port)
            connections.pop(str(message_tcp_port))
        else:
            connectedDevices[message_tcp_port]['sentMessages'] = decoded_message

            print(f"Sucesso: Mensagem UDP recebida de {message_tcp_port}!")

# Função responsável por receber as conexões.
def receive_connections():
    global tcpServer
    
    while True:
        connection, address = tcpServer.accept()
        threading.Thread(target=save_device, args=(connection, address)).start()
    
# Função responsável por iniciar o Broker e escutar as conexões.
def start_broker_server():
    global tcpServer
    global udpServer
    
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.bind(('localhost', tcpPort))
    tcpServer.listen(1)
    udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)
    udpServer.bind(('localhost', udpPort))
    
    print(f"TCP Server is listening on port {tcpPort}")
    print(f"UDP Server is listening on port {udpPort}")
    
    # Inicia a thread responsável pelo recebimento das conexões em segundo plano.
    threading.Thread(target=receive_connections).start()
    
    # Responsável pela escuta a todo momento das mensagens UDP enviadas pelos dispositivos.
    while (True):
        receive_udp_message(udpServer)