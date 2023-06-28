# Telegram bot for voice message download
## Description
This telegram bot is used to download voice message from telegram. You can send voice message directly or forward it to the bot.
## Installation:

1. Clone repository:
```
git clone git@github.com:RuselK/telegram_bot_audio_download.git
```

2. Create venv:
```
python3 -m venv venv
```

4. Run venv:

for linux:
```
source venv/bin/activate
```
for windows:
```
source venv/scripts/activate
```

5. Install dependences:
```
pip install -r requirements.txt
```

6. Create .env file and write telegram token:
 
```
touch .env 
```
```
nano .env 
```
Add following to your .env file:
```
TOKEN=<your_telegram_token>
```
7. Run the bot:
```
python3 main.py
```

## Included Libraries
1. [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
