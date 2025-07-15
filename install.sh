#!/bin/bash

# Carrega variáveis do .env
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi
source .env

# Valida se variáveis foram preenchidas
if [[ -z "$BOT_DIR" || -z "$BOT_SCRIPT" ]]; then
    echo "❌ Variáveis BOT_DIR ou BOT_SCRIPT não definidas corretamente no .env"
    exit 1
fi

SERVICE_NAME="maketeam"
SERVICE_TEMPLATE="maketeam.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# Verifica se discord.py está instalado
echo "🔍 Verificando se discord.py está instalado..."
python3 -c "import discord" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 discord.py está com instalação incompleta. Instalando novamente..."
    pip3 install discord.py
else
    echo "✅ discord.py já está instalado."
fi

# Verifica se python-dotenv está instalado
echo "🔍 Verificando se python-dotenv está instalado..."
python3 -c "import dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 python-dotenv não encontrado. Instalando..."
    pip3 install python-dotenv
else
    echo "✅ python-dotenv já está instalado."
fi

# Gera o arquivo de serviço systemd
echo "⚙️ Gerando arquivo de serviço em $SERVICE_FILE"
sed "s|\${BOT_DIR}|$BOT_DIR|g; s|\${BOT_SCRIPT}|$BOT_SCRIPT|g" "$SERVICE_TEMPLATE" > "$SERVICE_FILE"

if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ Falha ao criar arquivo de serviço systemd!"
    exit 1
fi

chmod 644 "$SERVICE_FILE"

echo "🔄 Recarregando systemd"
systemctl daemon-reload

echo "📌 Habilitando MakeTeam para iniciar com o sistema"
systemctl enable "$SERVICE_NAME"

echo "🚀 Iniciando o serviço MakeTeam"
systemctl start "$SERVICE_NAME"

echo "📊 Verificando status:"
systemctl status "$SERVICE_NAME" --no-pager
