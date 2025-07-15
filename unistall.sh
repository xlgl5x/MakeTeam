#!/bin/bash

SERVICE_NAME="maketeam"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "🛑 Parando e desabilitando o serviço do MakeTeam..."

# Para e desabilita o serviço
systemctl stop "$SERVICE_NAME" 2>/dev/null
systemctl disable "$SERVICE_NAME" 2>/dev/null

# Remove o arquivo systemd, se existir
if [ -f "$SERVICE_FILE" ]; then
    echo "🧹 Removendo o arquivo systemd $SERVICE_FILE..."
    rm -f "$SERVICE_FILE"
else
    echo "ℹ️ Arquivo de serviço systemd não encontrado."
fi

# Recarrega o systemd
echo "🔄 Recarregando systemd..."
systemctl daemon-reload
systemctl reset-failed

# Remove as bibliotecas Python usadas
echo "📦 Removendo bibliotecas Python (discord e python-dotenv)..."
pip3 uninstall -y discord discord.py python-dotenv

echo "✅ Uninstall finalizado com sucesso!"
