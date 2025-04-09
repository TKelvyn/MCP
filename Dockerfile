# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install fastmcp

# Expõe a porta que o servidor MCP usará
EXPOSE 8000

# Comando para executar o servidor
CMD ["python", "mcp_handler.py"] 
