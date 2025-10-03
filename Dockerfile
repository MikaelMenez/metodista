FROM python:3.11-slim

# Install curl and build-essential for Poetry
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instale Poetry (versão recomendada)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicione o Poetry ao PATH
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copie o pyproject.toml e poetry.lock se existir
COPY pyproject.toml poetry.lock* /app/

# Instale as dependências com Poetry sem instalar o ambiente virtual
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copie todo o código da app
COPY . .

# Exponha a porta
EXPOSE 8000

# Comando para rodar a aplicação (exemplo com uvicorn via poetry)
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
