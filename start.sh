#!/bin/bash

echo "Iniciando ambiente Kafka e MongoDB..."
docker-compose up -d

echo " Aguardando Kafka iniciar..."
sleep 10

echo "✅ Criando tópicos no Kafka..."
docker exec -it kafka kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1 || echo "Tópico já existe!"

echo "✅ Configurando MongoDB..."
python scripts/setup_mongodb.py

echo " Iniciando aplicação..."
docker-compose up -d app
