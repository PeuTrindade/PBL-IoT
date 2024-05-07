# Sistema de ar-condicionados - PBL Redes 01

O projeto descrito neste documento, possui como propósito emular um sistema de gerenciamento de ar-condicionados. Ele é composto por 3 subsistemas que devem funcionar em máquinas distintas de uma mesma rede, permitindo a troca de informações entre elas através do uso de protocolos de mensagem TCP/IP e UDP.

## 🚀 Overview do projeto

O projeto é composto por 3 subsistemas. O primeiro deles, consiste em uma interface que permite o usuário visualizar e gerenciar todos os ar-condicionados conectados. Dessa forma, é possível através dela ligar, desligar e alterar a temperatura de qualquer um dos dispositivos. Além disso, a interface oferece ao usuário a capacidade de visualizar um histórico de logs de cada comando emitido pelos ar-condicionados. Tal subsistema foi desenvolvido utilizando as tecnologias `ReactJS` e `Bootstrap`.

Já o segundo, consiste em um simples Broker de mensagens. Este produto tem como finalidade servir como o intermediário do sistema como um todo, pois ele gerencia o envio e o recebimento de informações de todos os ar-condicionados conectados. Este tipo de programa é amplamente utilizado em empresas que lidam com o envio de mensagens para inúmeros destinatários. Todo este subsistema foi desenvolvido utilizando a linguagem de programação `Python`.

Por fim, o terceiro subsistema simula um sensor de ar-condicionado. Este dispositivo é responsável por enviar de forma ininterrupta informações referentes a um ar-condicionado, tais como: modo (ligado/desligado), temperatura e logs. Este produto foi desenvolvido utilizando a linguagem de programação `Python`.

## 📋 Pré-requisitos

Para garantir o bom funcionamento do projeto em seu ambiente, é necessário que haja algumas ferramentas instaladas:

```
Docker
Python 3.10.5
Node
npm
```

## 🔧 Instalação

Esta seção irá explicar como rodar este projeto em sua máquina local. 

OBS: É possível visualizar o comportamento do sistema utilizando apenas uma máquina, ou uma máquina para cada subsistema. Porém, em caso de utilizar apenas uma, será possível a criação de apenas um ar-condicionado. Pois, cada ar-condicionado está atrelado à um endereço IP.

### 📦 Como baixar projeto:

1) Baixe o projeto como ZIP em sua máquina, ou clone o repositório:

```
git clone https://github.com/PeuTrindade/PBL-IoT.git
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

OBS: Os passos 2 e 3 são para o uso do Docker, caso deseje utilizar o node/npm execute:

```
npm install
npm start
```

### 📥 Como iniciar o Broker:

1) Acesse a pasta `MessageBroker`.

2) Execute o seguinte comando Docker:

```
docker build -t broker .
```

3) Em seguida, execute este comando:

```
docker run -p 4000:4000 -p 5000:5000/udp -p 5976:5976 broker
```

OBS: Os passos 2 e 3 são para o uso do Docker, caso deseje utilizar o python execute:

```
pip install -r requirements.txt
python MessageBroker.py
```

### 🖲️ Como iniciar o sensor:

1) Acesse a pasta `device`.

2) Execute o seguinte comando:

```
docker build -t device .
```

3) Em seguida, execute o seguinte comando:

```
docker run -it --name device device
```

OBS: Os passos 2 e 3 são para o uso do Docker, caso deseje utilizar o python execute:

```
pip install -r requirements.txt
python device.py
```

## Desenvolvimento do projeto

Visando garantir uma melhor compreensão acerca do produto apresentado neste documento, é de suma importância expor como foi ele desenvolvido, além de justificar cada decisão tomada durante a codificação. É válido mencionar que, devido ao sistema ser composto por subpartes, houve uma ordem de criação. Tal ordem foi: broker, dispositivo, e por fim a interface.

Antes de aprofundar sobre cada subsistema do produto, é necessário ter uma noção a respeito da arquitetura geral. O Broker, sendo um software de gerenciamento de mensagens, armazena as informações vitais do sistema, em uma estrutura de dados nomeada de dicionários. Ele organiza esses dados de acordo com as informações vindas dos dispositivos conectados a ele, que enviam seus estados de forma ininterrupta.

A interface, por sua vez, busca os dados contidos no Broker, através do envio de requisições para a API (Application Programming Interface) pertencente ao Broker. Segue abaixo um diagrama exemplificando a arquitetura geral do produto. (Ver figura 1)

![Figura 1](https://github.com/PeuTrindade/PBL-IoT/assets/84353169/58935acf-791b-40c1-90e5-df6d9e9f8de2)

Após a explanação a respeito da arquitetura geral do sistema, é importante destrinchar o Broker. Tal componente foi desenvolvido em dois arquivos distintos, utilizando a linguagem de programação Python. O primeiro deles contém a implementação de uma API, que será responsável por se comunicar com a interface, além da chamada da função principal do segundo arquivo, que irá iniciar o servidor de mensageria.

Dessa forma, o arquivo principal, nomeado de “MessageBroker”, deve ser iniciado para que o Broker entre em execução. Assim, após a inicialização, tanto o servidor da API, quanto o servidor de gerenciamento de mensagens estarão em funcionamento lado a lado. Segue abaixo um diagrama ilustrando essa interação. (Ver figura 2)

![Figura 2](https://github.com/PeuTrindade/PBL-IoT/assets/84353169/7c527115-f7aa-4407-a2f7-d8f4e69236bd)

No que se refere à API, ela é composta por algumas rotas que serão chamadas pela interface, ou alguma plataforma de teste de APIs (Insomnia ou Postman). Tais rotas são: “/devices”, “/change_mode/<port>/<mode>” e “/change_temperature/<port>/<temperature>”. Elas servem para enviar os dados dos dispositivos conectados, alterar o modo (Ligado ou desligado) de um dispositivo específico e alterar a temperatura de um dispositivo específico, respectivamente. (Ver figura 3)

![Figura 3](https://github.com/PeuTrindade/PBL-IoT/assets/84353169/aa828ad2-8919-4661-87cd-2cd14b093264)

Ao arquivo principal do Broker ser inicializado, é criada uma “thread” para executar o servidor de mensageria. Uma “thread” consiste em uma unidade básica de execução de um programa, que permite que diferentes partes do código sejam executadas simultaneamente. Dessa forma, foi necessária a utilização deste recurso para que a API e o servidor se mantivessem em funcionamento paralelamente sem conflitos.

Então, quando este servidor está em andamento, primeiramente são configurados os “sockets” (Recursos responsáveis por criar conexões entre diferentes computadores) para conexões TCP/IP e UDP. TCP/IP (Transmission Control Protocol) e UDP (User Datagram Protocol) são protocolos de comunicação, sendo o primeiro deles caracterizado pela entrega confiável e segura dos dados aos destinatários, enquanto o segundo é comumente utilizado para comunicações rápidas e eficientes, visto que não possui confiabilidade, podendo haver perda de informações. Ambos protocolos foram utilizados no Broker de acordo com os seus conceitos.

Após tais configurações serem implementadas, é iniciada uma “thread” responsável por receber conexões. Quando uma conexão é recebida, os dados do conector são salvos em um dicionário de dispositivos, criando como chave identificatória o IP da máquina em que o dispositivo está funcionando. Além disso, a conexão é salva em um outro dicionário, para facilitar possíveis comunicações futuras.
Além da thread mencionada acima, uma outra função se mantém em execução paralelamente. Ela tem como papel receber as mensagens vindas dos dispositivos em protocolo UDP. Assim, após uma mensagem ser capturada, é realizada uma lógica para verificar o endereço IP do emitente e o conteúdo, e por fim, é salvo no dicionário de dispositivos a informação recebida na localização do dispositivo que a enviou.

Existem ainda duas funções importantes pertencentes ao arquivo auxiliar do Broker. Tais funções são utilizadas quando as rotas de alteração de modo e temperatura são requisitadas. Basicamente, elas recebem como parâmetro o endereço IP do dispositivo que o usuário deseja modificar, e o valor a ser substituído. Então, busca-se no dicionário de conexões a conexão referente àquele endereço, e é enviada ao dispositivo uma mensagem via protocolo TCP/IP contendo o novo dado a ser inserido. 
Visando garantir segurança na implementação desses dois métodos, foi utilizado o protocolo TCP/IP, já que, trata-se de informações importantes que não podem ser perdidas. Segue abaixo um diagrama ilustrando todo o funcionamento do Broker. (Ver figura 4)

![Figura 4](https://github.com/PeuTrindade/PBL-IoT/assets/84353169/820cd89b-257a-4468-82a8-fffef68d97d6)

Após a conclusão da explanação a respeito do funcionamento do Broker, é válido abordar acerca do dispositivo. Tal subsistema, também desenvolvido com a linguagem de programação Python, é constituído por apenas um arquivo. A partir do momento em que este arquivo é iniciado, é requisitado ao usuário que ele preencha, via terminal, os dados de configuração do dispositivo. Tais dados são: nome do dispositivo, endereço IP do broker, porta de conexão TCP/IP e porta de conexão UDP.

Ao serem inseridas as informações mencionadas acima, e o dispositivo ser devidamente conectado ao Broker, são iniciadas duas threads. A primeira delas é uma thread responsável por enviar de forma ininterrupta um objeto contendo as informações do dispositivo, utilizando o protocolo UDP. Esse objeto contém os seguintes dados: nome do dispositivo, logs, modo e temperatura. Buscando possuir compatibilidade com os conceitos dos protocolos de comunicações, foi utilizado o UDP para essa funcionalidade, já que, essas informações serão enviadas a todo momento ao Broker, logo, não existe a necessidade de garantir confiabilidade e segurança.

A segunda thread, por sua vez, desempenha o papel de ouvir as mensagens vindas do Broker, via protocolo TCP/IP. Tais mensagens, são os dados recebidos pelo Broker pela API, quando algum usuário solicita por meio da interface, a alteração do modo do dispositivo ou a sua temperatura. Dessa forma, assim que uma mensagem é capturada por essa função, o valor recebido é substituído no objeto de informações do dispositivo.

Paralelamente a essas duas threads, existe uma funcionalidade responsável pelo gerenciamento de um menu interativo. A partir dele, o usuário consegue manipular os estados do dispositivo, através de comandos em linha de comando, tais como: ligar, desligar, alterar temperatura e visualizar estado atual. Segue abaixo um diagrama ilustrando o funcionamento do dispositivo. (Ver figura 5)

![Figura 5](https://github.com/PeuTrindade/PBL-IoT/assets/84353169/c5e40272-8c85-4db6-9628-08ef7787850a)

Por fim, foi implementada a interface visual para o usuário interagir com todos os dispositivos, utilizando as tecnologias ReactJS e Bootstrap. Basicamente, esta interface irá se comunicar com a API do Broker, buscando informações a respeito dos dispositivos e as exibindo. Além disso, ela permite o envio de comandos, tais como: ligar, desligar e alterar temperatura. Buscando garantir uma melhor experiência ao usuário, os dados são atualizados a cada segundo.

É importante comentar a respeito do desempenho da aplicação. De maneira geral, em um ambiente contendo uma boa conexão a internet, todos os subcomponentes conversam entre si com agilidade e eficiência. Foram elaborados alguns mecanismos para evitar lentidão e dados pesados, como por exemplo, limitação de logs dos dispositivos para apenas 10 registros, e aumento do buffer de mensagem na configuração do socket no Broker.

À respeito da confiabilidade do sistema, é correto afirmar que todos os subsistemas possuem. Dessa forma, é possível remover a conexão à internet e inseri-la novamente, e em alguns segundos o sistema se sincronizará sem perda de informações.

O Docker foi uma ferramenta bastante importante para o desenvolvimento. Ele permite a criação de imagens de aplicações em qualquer linguagem, e às sobe em um container virtual para a aplicação ser usada em qualquer máquina, mesmo que não possua as mesmas dependências e tecnologias usadas. Todos os subsistemas possuem um arquivo Docker, que irá permitir o seu uso em qualquer ambiente.
