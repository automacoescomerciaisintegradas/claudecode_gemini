#!/bin/bash
# Script de instalação completa do Multi-Agent Framework

set -e

echo "🚀 Instalando Multi-Agent Framework..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ Python 3.10+ necessário. Versão encontrada: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale Node.js 18+"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2)
echo "✅ Node.js $NODE_VERSION encontrado"

# Instalar dependências do backend
echo ""
echo "📦 Instalando dependências do backend Python..."
cd apps/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ../..

# Instalar dependências do frontend
echo ""
echo "📦 Instalando dependências do frontend..."
cd apps/frontend
npm install
cd ../..

# Instalar dependências root
echo ""
echo "📦 Instalando dependências root..."
npm install

# Instalar pre-commit hooks
echo ""
echo "🔧 Configurando pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
else
    echo "⚠️  pre-commit não encontrado. Pulando instalação de hooks."
fi

# Criar arquivo .env
if [ ! -f .env ]; then
    echo ""
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  Configure suas variáveis de ambiente em .env"
fi

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "📚 Próximos passos:"
echo "   1. Configure ANTHROPIC_API_KEY em .env"
echo "   2. Execute 'npm run dev' para modo desenvolvimento"
echo "   3. Execute 'npm start' para iniciar a aplicação"
echo ""
