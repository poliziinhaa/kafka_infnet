from confluent_kafka import Producer
import json
import time
from transaction_generator import TransactionGenerator 

# Configuração do Kafka Producer
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'fraud-detection-producer'
}

producer = Producer(conf)

# Criar gerador de transações
transaction_generator = TransactionGenerator(trans_per_sec=2)

def delivery_report(err, msg):
    """ Callback para indicar se a mensagem foi enviada com sucesso """
    if err is not None:
        print(f'Erro ao enviar mensagem: {err}')
    else:
        print(f'Mensagem enviada para {msg.topic()} [partição {msg.partition()}]')

# Produzindo mensagens para o Kafka
print("Iniciando produtor Kafka...")

try:
    for tx in transaction_generator.generate_transactions():
        tx_json = json.dumps(tx.__dict__)  
        producer.produce("transactions", value=tx_json, callback=delivery_report)
        producer.flush()  
        time.sleep(1)  

except KeyboardInterrupt:
    print("Produtor encerrado.")
finally:
    producer.flush()
