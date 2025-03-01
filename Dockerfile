# Usa a imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos do projeto para dentro do container
COPY . .

# Instala todas as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão para manter o container rodando
CMD ["streamlit", "run", "fraude_dashboard.py"]
