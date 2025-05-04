#!/bin/bash

set -e

# Aplica um delay para garantir que o banco de dados esteja pronto
delay=4

# Aplica as migrações
echo "Aplicando migrações..."
python manage.py migrate

# Executa os testes
echo "Executando testes do Django..."
if ! python manage.py test; then
  echo -e "\033[0;31m Alguns testes falharam! Corrija os erros antes de continuar.\033[0m"
fi

# Inicia o servidor
echo "Iniciando servidor Django..."
exec "$@"
