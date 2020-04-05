from pyrogram import Client
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from decouple import config
from handlers.basic import help_handler, start_handler, store_names_handler, less_handler, delete_handler
from handlers.leaderboards import taco_top_handler, my_tacos_handler
from handlers.setup import self_kick_handler, new_chat_handler
from handlers.tacotransfers import chat_reply_handler, taco_mention_handler, tacoinflator

scheduler = BackgroundScheduler()


bot_token = config('BOT_TOKEN')
api_id = config('API_ID', cast=int)
api_hash = config('API_HASH')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.getLevelName(config('LOG_LEVEL', default='INFO')))

bot = Client(session_name='TacoTestBot',
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


if __name__ == '__main__':

    scheduler.add_job(tacoinflator, trigger='cron', hour='0,12')

    bot.add_handler(new_chat_handler, group=-1)
    bot.add_handler(store_names_handler, group=-1)

    bot.add_handler(start_handler)
    bot.add_handler(help_handler)
    bot.add_handler(self_kick_handler)
    bot.add_handler(chat_reply_handler)
    bot.add_handler(my_tacos_handler)
    bot.add_handler(taco_top_handler)
    bot.add_handler(less_handler)
    bot.add_handler(taco_mention_handler)
    bot.add_handler(delete_handler)

    scheduler.start()
    bot.run()




