#!/bin/bash
# Script de build do Multi-Agent Framework

set -e

echo "🔨 Build do Multi-Agent Framework..."

# Build do backend
echo ""
echo "📦 Build do backend Python..."
python3 -m py_compile apps/backend/*.py
python3 -m py_compile apps/backend/agents/*.py
python3 -m py_compile apps/backend/qa_pipeline/*.py
python3 -m py_compile apps/backend/config/*.py
python3 -m py_compile apps/backend/utils/*.py
echo "✅ Backend compilado"

# Build do frontend
echo ""
echo "📦 Build do frontend Electron..."
cd apps/frontend
npm run build
cd ../..
echo "✅ Frontend compilado"

# Copiar arquivos para dist
echo ""
echo "📁 Organizando arquivos de distribuição..."
mkdir -p dist
cp -r apps/frontend/dist/* dist/
cp -r apps/backend dist/backend
cp run.py dist/
cp package.json dist/

echo ""
echo "✅ Build concluído!"
echo "📁 Arquivos em: dist/"
