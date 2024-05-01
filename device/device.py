import socket
import json
import time
import threading
import atexit
import datetime
import pickle
import os

clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

brokerIPAdress = None
brokerPortTCP = None
brokerPortUDP = None
deviceName = None

# Estado do dispositivo.
device_state = {"on": False, "temperature": 25, "deviceName": None, "logs": []}

# Salva em um arquivo binário o último estado do dispositivo.
def save_last_state():
    global device_state
    
    with open('last_state.bin', 'wb') as file:
        pickle.dump(device_state, file)

# Ler do arquivo binário o último estado do dispositivo.    
def get_last_state():
    global device_state
    
    if os.path.exists('last_state.bin'):
        with open('last_state.bin', 'rb') as file:
            loaded_data = pickle.load(file)
            
            if loaded_data:
                loaded_data['on'] = False
                device_state = loaded_data

# Função responsável por enviar estado do dispositivo em UDP.
def send_device_state_to_server():
    global brokerPortUDP, brokerIPAdress
    
    while True:
        # Caso o número de logs seja maior que 10, o array de logs é resetado, mantendo apenas o último registro.
        if len(device_state['logs']) > 10:
            device_state['logs'] = [device_state['logs'][len(device_state['logs']) - 1]]
            
        clientUDP.sendto(json.dumps(device_state).encode(), (brokerIPAdress, int(brokerPortUDP)))
   
# Função responsável por enviar pela última vez o estado do dispositivo, quando o programa é encerrado.     
def change_device_to_inactive():
    global brokerPortUDP, brokerIPAdress
    
    # É enviado o estado None, para indicar que o dispositivo está inativo.
    device_state['on'] = None
    
    # Caso o número de logs seja maior que 10, o array de logs é resetado, mantendo apenas o último registro.
    if len(device_state['logs']) > 10:
        device_state['logs'] = [device_state['logs'][len(device_state['logs']) - 1]]
    
    # Armazena o último estado do dispositivo em um arquivo binário.
    save_last_state()
    clientUDP.sendto(json.dumps(device_state).encode(), (brokerIPAdress, int(brokerPortUDP)))

# Função responsável por printar o menu.
def print_menu():
    print("\033[34m" + "===================================\nMenu:\n")
    print("[1] -> Ligar dispositivo")
    print("[2] -> Alterar temperatura")
    print("[3] -> Exibir estado atual")
    print("[4] -> Desligar dispositivo")
    print("===================================" + "\033[0m")
    
    selected_option = input("Escolha uma opção: ")
    
    return selected_option

# Função responsável por gerenciar o menu e escolhas do usuário.
def start_menu():
    selected_option = print_menu()
    
    while True:
        if selected_option == '1':
            device_state['on'] = True
            
            device_state['logs'].append({
                "date": str(datetime.datetime.now()),
                "message": "O dispositivo foi ligado!"
            })

            print("\033[32m" + "Sucesso: Ar condicionado ligado com sucesso!" + "\033[0m")
            
        elif selected_option == '2':
            if device_state['on']:
                temperature = input("Insira uma temperatura (Valor inteiro): ")
                
                if temperature and temperature.isdigit():
                    device_state['temperature'] = int(temperature)
                    
                    device_state['logs'].append({
                        "date": str(datetime.datetime.now()),
                        "message": f"A temperatura foi alterada para {temperature} graus!"
                    })
                    
                    print("\033[32m" + f"Sucesso: Temperatura alterada com sucesso para {temperature} graus!" + "\033[0m")
                else:
                    print("\033[31m" + "Erro: Por favor, insira uma temperatura válida!" + "\033[0m")
            else:
                print("\033[31m" + "Erro: Por favor, ligue o dispositivo!" + "\033[0m")
        
        elif selected_option == '3':
            if device_state['on'] == True:
                print("\033[33m" + f"Modo: Ligado | Temperatura: {device_state['temperature']}" + "\033[0m" + "\n")
            else:
                print("\033[33m" + f"Modo: Desligado | Temperatura: {device_state['temperature']}" + "\033[0m" + "\n")
        
        elif selected_option == '4':
            device_state['on'] = False
            
            device_state['logs'].append({
                "date": str(datetime.datetime.now()),
                "message": "O dispositivo foi inativado!"
            })

            print("\033[32m" + "Sucesso: Ar condicionado desligado com sucesso!" + "\033[0m")
            
        selected_option = print_menu()

# Função responsável por escutar mensagens TCP do servidor em segundo plano.
def listen_to_server():
    global clientTCP
    
    while True:
        try:
            message = clientTCP.recv(1024).decode()
            if message:
                if message == 'on' or message == 'off':
                    if message == 'on':
                        device_state['on'] = True
                        device_state['logs'].append({
                            "date": str(datetime.datetime.now()),
                            "message": "O dispositivo foi ligado pelo servidor!"
                        })
                    else:
                        device_state['on'] = False
                        device_state['logs'].append({
                            "date": str(datetime.datetime.now()),
                            "message": "O dispositivo foi desligado pelo servidor!"
                        })
                else:
                    device_state['temperature'] = int(message)
                    device_state['logs'].append({
                        "date": str(datetime.datetime.now()),
                        "message": f"A temperatura foi alterada para {message} graus pelo servidor!"
                    })
        except Exception as e:
            print("Erro ao receber mensagem TCP:", e)
            break

# Função responsável por enviar a primeira mensagem ao usuário.
def send_greeting_messages():
    global brokerPortTCP, brokerPortUDP, brokerIPAdress, deviceName
    
    # Caso haja algum estado passado armazenado, é carregado.
    get_last_state()
    
    print("\033[36m" + "===================================\nAr condicionado iniciado!\n===================================" + "\033[0m")

    print("\033[34m" + "===================================\nConfigure o seu dispositivo\n")

    deviceName = input("Insira o nome do dispositivo: ")
    brokerIPAdress = input("Insira o endereço IP do broker: ")
    brokerPortTCP = input("Insira a porta do servidor TCP: ")
    brokerPortUDP = input("Insira a porta do servidor UDP: ")

    print("==================================="  + "\033[0m")

    clientTCP.connect((brokerIPAdress, int(brokerPortTCP)))
    clientUDP.connect((brokerIPAdress, int(brokerPortUDP)))
    
    device_state['deviceName'] = deviceName

    message = clientTCP.recv(1024).decode()

    while (message == ''):
        message = clientTCP.recv(1024).decode()
    
    print("\033[32m" + f"Mensagem do servidor: {message}" + "\033[0m")
    
    # Iniciar a thread para enviar estado do dispositivo ao Broker em segundo plano.
    udp_message_send = threading.Thread(target=send_device_state_to_server)
    udp_message_send.daemon = True
    udp_message_send.start()
    
    # Iniciar a thread para escutar mensagens TCP em segundo plano
    tcp_listener_thread = threading.Thread(target=listen_to_server)
    tcp_listener_thread.daemon = True
    tcp_listener_thread.start()
    
    start_menu()

# Registrando a função de inatividade como última ao programa ser encerrado.
atexit.register(change_device_to_inactive)

if __name__ == "__main__":
    send_greeting_messages()