import socket
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import json
import sys
sys.path.append('utils')
from auxFunctions import start_broker_server, connectedDevices, change_device_mode, change_device_temperature

app = Flask(__name__)

# Adicionando CORS na API, para funcionar em ambiente WEB.
CORS(app)

# Rota responsável pelo retorno de todos os dispositivos cadastrados no Broker.
@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(connectedDevices), 200

# Rota responsável pela mudança de modo de um dispositivo registrado.
@app.route('/change_mode/<port>/<mode>', methods=['PATCH'])
def send_mode_command(port, mode):
    try:
        if mode == 'on' or mode == 'off':
            change_device_mode(port, mode)
        
            return jsonify({ "message": "Ok"}), 200
        else:
            return jsonify({ "message": "Envie um comando válido!"}), 400
    except e:
        return jsonify({ "message": "Falha ao enviar comando!"}), 500

# Rota responsável pela mudança de temperatura de um dispositivo registrado.
@app.route('/change_temperature/<port>/<temperature>', methods=['PATCH'])
def send_temperature_command(port, temperature):
    try:
        if temperature and str(temperature).isdigit():
            change_device_temperature(port, temperature)
        
            return jsonify({ "message": "Ok"}), 200
        else:
            return jsonify({ "message": "Envie um comando de temperatura válido!"}), 400
    except e:
        return jsonify({ "message": "Falha ao enviar comando!"}), 500

if __name__ == '__main__':
    # Inicia a thread para o servidor como broker.
    broker_thread = threading.Thread(target=start_broker_server)
    broker_thread.start()
    
    # Inicia o servidor Flask.
    app.run()