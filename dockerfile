FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Instala dependências
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
