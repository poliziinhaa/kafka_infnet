from confluent_kafka import Consumer
from pymongo import MongoClient
import json
import time
import random

# Conectar ao MongoDB
mongo_client = MongoClient("mongodb://admin:admin@localhost:27017/")
mongo_db = mongo_client["kafka_fraudes_v2"]
fraudes_collection = mongo_db["transacoes_suspeitas"]

# Configuração do Kafka
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'fraud-detection-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['transactions'])

print("Consumidor rodando...")

# 🔹 Mapeamento Correto de Países, Estados e Cidades
location_data = {
    "Brasil": {
        "SP": ["São Paulo", "Campinas", "Santos"],
        "RJ": ["Rio de Janeiro", "Niterói", "Petrópolis"],
        "MG": ["Belo Horizonte", "Uberlândia", "Contagem"],
        "PR": ["Curitiba", "Londrina", "Maringá"]
    },
    "USA": {
        "NY": ["New York", "Buffalo", "Albany"],
        "CA": ["Los Angeles", "San Francisco", "San Diego"],
        "FL": ["Miami", "Orlando", "Tampa"]
    },
    "Germany": {
        "BE": ["Berlin", "Potsdam", "Cottbus"],
        "BW": ["Stuttgart", "Karlsruhe", "Freiburg"]
    }
}

def get_valid_location(country):
    """ Seleciona uma cidade e estado válidos para o país """
    if country in location_data:
        state = random.choice(list(location_data[country].keys()))
        city = random.choice(location_data[country][state])
        return {"city": city, "state": state, "country": country}
    return {"city": "Desconhecido", "state": "Desconhecido", "country": country}

def check_fraud(transaction):
    """ Aplica regras de fraude e retorna as regras detectadas """
    user_id = transaction["user_id"]
    value = transaction["value"]
    timestamp = transaction["timestamp"]
    country = transaction["country"]

    if user_id not in user_transactions:
        user_transactions[user_id] = []

    user_history = user_transactions[user_id]
    fraud_detected = []

    # Regra 1: Alta Frequência
    if len(user_history) > 1:
        last_tx = user_history[-1]
        time_diff = timestamp - last_tx["timestamp"]
        if time_diff < 300 and value != last_tx["value"]:
            fraud_detected.append("Alta Frequência")

    # Regra 2: Alto Valor
    if user_history:
        max_past_value = max(tx["value"] for tx in user_history)
        if value > max_past_value * 2:
            fraud_detected.append("Alto Valor")

    # Regra 3: Outro País
    if len(user_history) > 1:
        last_tx = user_history[-1]
        time_diff = timestamp - last_tx["timestamp"]
        if time_diff < 7200 and last_tx["country"] != country:
            fraud_detected.append("Outro País")

    user_transactions[user_id].append(transaction)
    return fraud_detected

# Estrutura para armazenar histórico de transações
user_transactions = {}

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        transaction = json.loads(msg.value().decode('utf-8'))
        country = transaction["country"]

        # 🔹 Corrigir localização
        location = get_valid_location(country)

        enriched_transaction = {
            "user_id": transaction["user_id"],
            "card_id": transaction["card_id"],
            "timestamp": int(time.time()),
            "value": transaction["value"],
            "location": location,
            "rule_detected": check_fraud(transaction),
            "site_id": transaction["site_id"],
            "merchant_category": random.choice(["e-commerce", "restaurante", "hotelaria", "transporte"])
        }

        if enriched_transaction["rule_detected"]:
            fraudes_collection.insert_one(enriched_transaction)
            print(f"🚨 FRAUDE DETECTADA: {enriched_transaction}")

except KeyboardInterrupt:
    print("Encerrando consumidor...")
finally:
    consumer.close()
