import logging
import os
import sys
from io import BytesIO

from dotenv import load_dotenv
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)

from exceptions import MissingEnvironmentVariable

load_dotenv()

TOKEN = os.getenv('TOKEN')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] '
    'line: %(lineno)d in %(funcName)s, '
    '%(message)s'
)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def check_token():
    """Check access to TOKEN."""
    logger.debug('Function is started.')
    if TOKEN is None:
        logger.critical('Missing telegram TOKEN.')
        raise MissingEnvironmentVariable(
            'Missing telegram TOKEN.')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.debug('Function is started.')
        chat_id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text='Send or reply voice message to download it.'
        )
        logger.info(f'Message sent to chat_id {chat_id}.')
    except TelegramError:
        raise TelegramError()


async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    file = await bot.getFile(update.message.voice.file_id)
    voice_file = await context.bot.get_file(file)
    voice_bytes = await voice_file.download_as_bytearray()
    return voice_bytes


async def download_voice_message(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    try:
        logger.debug('Function is started.')
        chat_id = update.effective_chat.id
        voice = await download_file(update, context)

        await context.bot.send_document(
            chat_id=chat_id,
            document=BytesIO(voice),
            filename=f'{update.message.voice.file_id}.mp3'
        )

        logger.info(f'Message sent to chat_id {chat_id}.')
    except TelegramError:
        raise TelegramError()


def main():
    check_token()
    application = ApplicationBuilder().token(TOKEN).build()
    try:

        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(
            filters.VOICE, download_voice_message
        ))

        application.run_polling()
    except Exception as error:
        logger.error(error, exc_info=True)


if __name__ == '__main__':
    main()
