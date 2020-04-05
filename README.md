# TacoBot for Telegram

This is a port of HeyTaco Bot (Slack) for Telegram.


## Prerequisites

In order to run this bot you need to create `.env`-file inside of project folder. This file must contains such data as  
- `[BOT_TOKEN]`
- `[API_ID]`
- `[API_HASH]`
- `[BOT_USERNAME]`  
  
You can obtain `[BOT_TOKEN]` by contacting [@BotFather](https://t.me/botfather) and `[API_ID]/[API_HASH]` on [Telegram\'s website](https://my.telegram.org/). 
`BOT_USERNAME` must be bot's username with all upper- and lowercase letters in it,  without @sign in the beginning.  
  
`Example of .env file:`  
BOT_TOKEN=000:AaaAA-BbbBbBb\
API_ID=12345  
API_HASH=a1b2c3e  
BOT_USERNAME=HeyTacoBot

## Installation

This Project supports [Docker](https://www.docker.com/) containers. 


Assuming Docker, clone repo and create `.env` file inside of it. Then:
1. `docker build -t taco_bot .`
2. `docker run -d taco_bot`


## Usage

Send /start to bot.

Add it to your group and give it admin rights, so that it will be able to access messages.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

python-telegram-bot 
Docker 
HeyTacoBot
