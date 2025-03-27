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
