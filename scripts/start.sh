#!/bin/bash
# Script de inicialização do Multi-Agent Framework

set -e

echo "🚀 Iniciando Multi-Agent Framework..."

# Carregar variáveis de ambiente
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Ativar venv do backend
if [ -d "apps/backend/venv" ]; then
    source apps/backend/venv/bin/activate
fi

# Iniciar backend em background
echo "📡 Iniciando backend..."
python3 apps/backend/spec_runner.py &
BACKEND_PID=$!

# Aguardar backend iniciar
sleep 2

# Iniciar frontend
echo "🖥️  Iniciando frontend Electron..."
npm start

# Cleanup ao sair
trap "kill $BACKEND_PID 2>/dev/null || true" EXIT
