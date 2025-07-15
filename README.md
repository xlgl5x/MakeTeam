### 🔄 Versão 2.0.0 - 2024-07-08

#### 🚀 Funcionalidades adicionadas
**Tipo:** Minor

- Suporte para dois MIXs (`mix1` e `mix2`)
- Comando `!make update` para criar/ajustar canais automaticamente
- Melhorias no tratamento de erros (comandos inválidos)
- Mensagens mais claras no embed de ajuda (`!comandos`)
- Instalação automatizada via `install.sh` e suporte completo a `.env`

---

# MakeTeam Bot - CS2 Discord

Bot para Discord que organiza automaticamente partidas de **Counter-Strike 2**, separando jogadores em equipes e gerenciando canais de voz.

---

## 🎯 Funcionalidades

- Sorteio automático de equipes (até 5x5 + fila de espera)
- Movimentação automática entre canais de voz
- Comando para criar ou atualizar canais do Discord
- Lista de comandos integrada (`!comandos`)
- Serviço `systemd` com `.env` configurável para uso persistente

---

## 🚀 Comandos

| Comando             | Descrição                                                                 |
|---------------------|---------------------------------------------------------------------------|
| `!make mix1`        | Cria equipes usando os canais `[MIX 1]`                                   |
| `!make mix2`        | Cria equipes usando os canais `[MIX 2]`                                   |
| `!make update`      | Cria/atualiza os canais de voz padrão para MIX 1 e MIX 2                  |
| `!move mix1`        | Move todos os membros das equipes do MIX 1 de volta para o LOBBY          |
| `!move mix2`        | Move todos os membros das equipes do MIX 2 de volta para o LOBBY          |
| `!comandos`         | Exibe a lista de comandos disponíveis                                     |

---

## 🛠️ Requisitos

- Python 3.8+
- Bibliotecas Python:
  - `discord.py`
  - `python-dotenv`

Instale todas com:

```bash
pip install -r requirements.txt
```

---

## 📁 Estrutura Recomendada no Discord

```
Canais de voz:
├─ [MIX 1] - LOBBY
├─ [MIX 1] - EQUIPE 1
├─ [MIX 1] - EQUIPE 2
├─ [MIX 2] - LOBBY
├─ [MIX 2] - EQUIPE 1
├─ [MIX 2] - EQUIPE 2
└─ FILA DE ESPERA
```

---

## 🧠 Guia de Instalação Automática

### 1. Edite o `.env`

Abra e configure o arquivo `.env` com:

```env
# Caminho do diretório do bot
BOT_DIR=/caminho/absoluto/para/MakeTeam

# Nome do script do bot
BOT_SCRIPT=MakeTeam.py

# Token do seu bot do Discord
DISCORD_BOT_TOKEN=seu_token_aqui
```

Você pode usar o `.env.example` como modelo:

```bash
cp .env.example .env
```

---

### 2. Execute o script de instalação

```bash
chmod +x install.sh
./install.sh
```

Esse script:
- Copia `maketeam.service` para o systemd
- Ativa o serviço no boot
- Inicia o bot automaticamente

---

### 3. Verificar status do serviço

```bash
systemctl status maketeam
```

Se estiver tudo certo, verá o bot como “ativo” e rodando.

---

### 4. Logs do serviço

Para ver os logs em tempo real:

```bash
journalctl -u maketeam -f
```

---

## 👨‍💻 Autor

**Luiz Gustavo Lobo Simões**  
Gestor de Redes, Desenvolvedor de Bots e Apaixonado por CS  
🔗 [LinkedIn](https://www.linkedin.com/in/lgl5)

---

## ⚖️ Licença

MakeTeam © 2025 - lgl5
