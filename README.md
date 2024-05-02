# Sistema de ar-condicionados - PBL Redes 01

O projeto descrito neste documento, possui como propósito emular um sistema de gerenciamento de ar-condicionados. Ele é composto por 3 subsistemas que devem funcionar em máquinas distintas de uma mesma rede, permitindo a troca de informações entre elas através do uso de protocolos de mensagem TCP/IP e UDP.

## 🚀 Overview do projeto

O projeto é composto por 3 subsistemas. O primeiro deles, consiste em uma interface que permite o usuário visualizar e gerenciar todos os ar-condicionados conectados. Dessa forma, é possível através dela ligar, desligar e alterar a temperatura de qualquer um dos dispositivos. Além disso, a interface oferece ao usuário a capacidade de visualizar um histórico de logs de cada comando emitido pelos ar-condicionados. Tal subsistema foi desenvolvido utilizando as tecnologias `ReactJS` e `Bootstrap`.

Já o segundo, consiste em um simples Broker de mensagens. Este produto tem como finalidade servir como o intermediário do sistema como um todo, pois ele gerencia o envio e o recebimento de informações de todos os ar-condicionados conectados. Este tipo de programa é amplamente utilizado em empresas que lidam com o envio de mensagens para inúmeros destinatários. Todo este subsistema foi desenvolvido utilizando a linguagem de programação `Python`.

Por fim, o terceiro subsistema simula um sensor de ar-condicionado. Este dispositivo é responsável por enviar de forma ininterrupta informações referentes a um ar-condicionado, tais como: modo (ligado/desligado), temperatura e logs. Este produto foi desenvolvido utilizando a linguagem de programação `Python`.

## 🔧 Instalação

Esta seção irá explicar como rodar este projeto em sua máquina local. 

OBS: É possível visualizar o comportamento do sistema utilizando apenas uma máquina, ou uma máquina para cada subsistema. Porém, em caso de utilizar apenas uma, será possível a criação de apenas um ar-condicionado. Pois, cada ar-condicionado está atrelado à um endereço IP.

### 📦 Como baixar projeto:

1) Baixe o projeto como ZIP em sua máquina, ou clone o repositório:

```

git clone https://github.com/PeuTrindade/PBL-IoT

```

2) Acesse pelo terminal o projeto `PBL-IOT`.

### 💻 Como iniciar a interface:

1) Inicie o Docker em sua máquina.

2) Acesse a pasta `frontend` e execute o seguinte comando Docker:

```

docker build -t frontend .

```

3) Em seguida, execute este comando:

```

docker run --name frontend -p 3000:3000 frontend

```

### 📥 Como iniciar o Broker:

1) Acesse a pasta `MessageBroker`.

2) Execute o seguinte comando:

```

python MessageBroker.py

```

### 🖲️ Como iniciar o sensor:

1) Acesse a pasta `device`.

2) Execute o seguinte comando:

```

python device.py

```
