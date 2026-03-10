#!/bin/bash
# Script de testes do Multi-Agent Framework

set -e

echo "🧪 Rodando testes do Multi-Agent Framework..."

# Testes do backend
echo ""
echo "🐍 Testes do backend Python..."
cd apps/backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
pytest -v --cov=. --cov-report=term-missing
cd ../..

# Testes do frontend
echo ""
echo "⚛️  Testes do frontend React..."
cd apps/frontend
npm test
cd ../..

echo ""
echo "✅ Todos os testes concluídos!"
