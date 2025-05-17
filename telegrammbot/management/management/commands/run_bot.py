import asyncio
import logging

from telebot import util
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tgbot.main_bot import bot

logger=logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        try:
            asyncio.run(bot.infinity_polling(logger_level=settings.LOG_LEVEL,allowed_updates=util.update_types))
        except Exception as err:
            logger.error(f'ОШИБКА{err}')