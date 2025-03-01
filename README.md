# 🏦 Sistema de Detecção de Fraude com Kafka e MongoDB

Este projeto implementa um sistema de detecção de fraudes em transações financeiras em tempo real utilizando **Apache Kafka**, **MongoDB** e **Streamlit** para visualização dos dados. O objetivo é processar transações de cartões de crédito e identificar atividades suspeitas com base em regras pré-definidas.

## 🚀 Tecnologias Utilizadas

- **Apache Kafka** → Processamento de mensagens em tempo real
- **MongoDB** → Armazenamento das transações e fraudes detectadas
- **Python 3.9** → Processamento e análise de dados
- **Streamlit** → Visualização interativa dos resultados
- **Docker & Docker-Compose** → Gerenciamento dos serviços

## 📂 Estrutura do Projeto

```
materia_kafka/
│── dashboard/              # Aplicação Streamlit para visualização
│── scripts/                # Scripts principais do projeto
│── .gitignore              # Arquivos ignorados no Git
│── docker-compose.yml      # Configuração do Docker
│── Dockerfile              # Configuração do ambiente Python no Docker
│── README.md               # Documentação do projeto
```

## 🛠️ Requisitos e Instalação

1. **Clone o repositório e entre na pasta do projeto**:
   ```bash
   git clone https://github.com/seu-usuario/materia_kafka.git
   cd materia_kafka
   ```
2. **Crie um ambiente virtual e instale as dependências**:
   ```bash
   python -m venv kafka
   source kafka/bin/activate  # Linux/Mac
   kafka\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

## 🐳 Configuração e Execução com Docker

1. **Suba os serviços do Kafka e MongoDB**:
   ```bash
   docker-compose up -d
   ```
2. **Verifique se os serviços estão rodando**:
   ```bash
   docker ps
   ```
3. **Criar o tópico no Kafka**:
   ```bash
   docker exec -it materia_kafka-kafka-1 kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
   ```

## 🔧 Execução do Projeto

1. **Iniciar o Kafka Producer**:
   ```bash
   python scripts/kafka_producer.py
   ```
2. **Iniciar o Kafka Consumer**:
   ```bash
   python scripts/kafka_consumer.py
   ```
3. **Rodar o Dashboard Streamlit**:
   ```bash
   streamlit run dashboard/app.py
   ```

## 📜 Licença

Este projeto é open-source e distribuído sob a licença MIT.

