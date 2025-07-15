#!/bin/bash

# Caminho do arquivo de changelog ou README com a versão
CHANGELOG_PATH="README.md"

# Verifica se o changelog existe
if [ ! -f "$CHANGELOG_PATH" ]; then
  echo "❌ Arquivo changelog não encontrado em:"
  echo "$CHANGELOG_PATH"
  exit 1
fi

# Extrai a primeira linha que contém a versão
VERSION_LINE=$(head -n 1 "$CHANGELOG_PATH")

# Extrai a versão usando regex
VERSION=$(echo "$VERSION_LINE" | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+')

if [ -z "$VERSION" ]; then
  echo "❌ Não foi possível identificar a versão atual."
  exit 1
fi

echo "📦 Versão detectada: v$VERSION"

# Verifica se é um repositório Git
if [ ! -d .git ]; then
  echo "❌ Este diretório não é um repositório Git válido."
  exit 1
fi

# Adiciona todas as alterações
git add .

# Solicita mensagem do commit
read -p '📝 Descreva o que foi alterado: ' MENSAGEM

# Comita com a versão incluída
git commit -m "Atualização v$VERSION - $MENSAGEM"

# Identifica a branch atual
BRANCH=$(git branch --show-current)

# Push para a branch atual
git push origin "$BRANCH"

echo "✅ Deploy enviado com sucesso para a branch '$BRANCH' com versão v$VERSION"
