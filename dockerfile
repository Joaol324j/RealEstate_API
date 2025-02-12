# Usar uma imagem base oficial do Python
FROM python:3.11

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos de dependências para o container
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta usada pelo FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]