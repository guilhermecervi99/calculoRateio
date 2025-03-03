# Usando Python 3.12 como base
FROM python:3.12

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto para dentro do container
COPY . .

# Definir o comando padrão para rodar a aplicação
CMD ["python", "src/main.py"]
