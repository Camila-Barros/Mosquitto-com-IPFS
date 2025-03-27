# Mosquitto-com-IPFS
Projeto capturando mensagens MQTT (via Mosquitto) e armazenando no IPFS

## Pŕe-requisitos:

✅ Ubuntu 24.04

✅ IPFS instalado 

✅ Mosquitto MQTT Broker 

✅ Python 3 


## 1. Instalar e Configurar o Mosquitto

<b>1.1 Instalar Mosquitto Broker + Client</b>

  ```bash
    sudo apt update
    sudo apt install mosquitto mosquitto-clients -y
  ```

<b>1.2 Iniciar e Habilitar o Mosquitto</b>

  ```bash
    sudo systemctl start mosquitto
    sudo systemctl enable mosquitto
  ```

<b>1.3 Testar o Mosquitto</b>

Subscrever ao tópico:

  ```bash
    mosquitto_sub -h localhost -t "TOPICO"
  ```

Publicar uma mensagem:

  ```bash
    mosquitto_pub -h localhost -t "TOPICO" -m "Hello MQTT e IPFS!"
  ```

Se a mensagem aparecer, o Mosquitto está funcionando.


## 2. Criar um Ambiente Virtual

A partir do Ubuntu 23.10 e 24.04, a política de gerenciamento de pacotes Python foi alterada para evitar conflitos entre pip e o gerenciador de pacotes apt. A solução é criar um ambiente virtual Python para instalar as dependências sem afetar o sistema.

<b>2.1 Instalar python3-venv (se não estiver instalado)</b>

  ```bash
    sudo apt install python3-venv python3-full -y
  ```

<b>2.2 Criar e ativar o ambiente virtual</b>

  ```bash
    python3 -m venv ~/ipfs-mqtt-venv  # Cria o ambiente
    source ~/ipfs-mqtt-venv/bin/activate  # Ativa o ambiente
  ```

  ➡ O prompt do terminal deverá mostrar (ipfs-mqtt-venv) no início da linha de comando.

<b>2.3 Instalar Dependências no Ambiente Virtual</b>

  ```bash
    pip install --upgrade pip
    pip install paho-mqtt ipfshttpclient
  ```

<b>2.4 Ativar o ambiente virtual </b>

  ```bash
    source ~/ipfs-mqtt-venv/bin/activate
  ```





## 3. Criar um Script Python para IPFS + Mosquitto

Python será usado para:
- Assinar um tópico MQTT.
- Salvar as mensagens em um arquivo.
- Enviar para o IPFS periodicamente.

<b>3.1 Instalar Dependências</b>

  ```bash
    pip install paho-mqtt requests
  ```

<b>3.2 Criar o Script no Visual Studio Code</b>

Nome do Script = mqtt_to_ipfs_http.py

  ```bash
    import paho.mqtt.client as mqtt
    import requests
    import time
    from datetime import datetime
    
    # Configurações MQTT
    MQTT_BROKER = "localhost"
    MQTT_TOPIC = "sensores/#"
    
    # Configurações IPFS (API HTTP padrão)
    IPFS_API_URL = "http://127.0.0.1:5001/api/v0"
    
    # Arquivo de log
    LOG_FILE = "mqtt_logs.txt"
    
    # Função para adicionar arquivo ao IPFS via HTTP
    def add_to_ipfs(file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{IPFS_API_URL}/add", files=files)
                return response.json()['Hash']
        except Exception as e:
            print(f"Erro ao adicionar ao IPFS: {e}")
            return None
    
    # Callback quando uma mensagem MQTT é recebida
    def on_message(client, userdata, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {msg.topic}: {msg.payload.decode()}\n"
        
        # Salva no arquivo de log
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        
        print(f"Log salvo: {log_entry.strip()}")
    
    # Configuração do cliente MQTT
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe(MQTT_TOPIC)
    
    # Envia logs para o IPFS a cada 30 segundos
    def upload_to_ipfs():
        while True:
            time.sleep(30)
            cid = add_to_ipfs(LOG_FILE)
            if cid:
                print(f"Uploaded to IPFS! CID: {cid}")
                print(f"Acesse em: http://localhost:8080/ipfs/{cid}")
    
    # Inicia o loop
    client.loop_start()
    upload_to_ipfs()
  ```

Selecionar o Interpretador Python Correto

  - Abra a Paleta de Comandos no VSCode (Ctrl + Shift + P).

  - Digite e selecione:
    Python: Select Interpreter

  - Escolha o interpretador do ambiente virtual:
    
    → Exemplo: ~/ipfs-mqtt-venv/bin/python3


Para evitar o problema no futuro:

  - Crie um arquivo .vscode/settings.json na pasta do projeto com:
      ```bash
        {
        "python.defaultInterpreterPath": "~/ipfs-mqtt-venv/bin/python3"
        }
      ```
  - Isso garante que o VSCode sempre use o ambiente virtual correto.


## 4. Executar o Sistema

<b>3.1 Iniciar o IPFS Daemon</b>

  ```bash
    ipfs daemon
  ```

<b>3.2 Rodar o Script Python diretamente no terminal do VSCode (com o venv ativo)</b>

  ```bash
    python3 mqtt_to_ipfs_http.py
  ```

<b>3.3 Testar Publicando uma Mensagem</b>

  ```bash
    mosquitto_pub -h localhost -t "sensores/temperatura" -m "45°C"
  ```

<b>3.4 Acesse via gateway:</b>

  ```bash
    http://localhost:8080/ipfs/<CID>
  ```

![image](https://github.com/Camila-Barros/Mosquitto-com-IPFS/blob/main/img1.png)


<b>3.5 Funcionamento Esperado</b>

O script irá:

- As mensagens MQTT são salvas em mqtt_logs.txt
- A cada 30 segundos, o arquivo é enviado ao IPFS via API HTTP
- O CID do arquivo é exibido no terminal, com um link para acesso via gateway local.

  



## Autora

Eng. Camila Cabral de Barros

Mestranda em Inovação Tecnológica pela UNIFESP

[Lattes](http://lattes.cnpq.br/2066462797590469)






