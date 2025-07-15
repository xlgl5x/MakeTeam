#!/bin/bash
echo "Copiando serviço para /etc/systemd/system/maketeam.service"
cp maketeam.service /etc/systemd/system/maketeam.service

echo "Recarregando systemd"
systemctl daemon-reexec

echo "Habilitando MakeTeam para iniciar com o sistema"
systemctl enable maketeam

echo "Iniciando o serviço MakeTeam"
systemctl start maketeam

echo "Verificando status:"
systemctl status maketeam --no-pager
