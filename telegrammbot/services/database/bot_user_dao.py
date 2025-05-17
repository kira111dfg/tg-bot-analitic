import logging

from asgiref.sync import sync_to_async
from telebot.types import Chat,User

from tgbot.models import BotUser
logger = logging.getLogger(__name__)

@sync_to_async
def update_or_create_tg_user(data:Chat|User):
    try:
        data = getattr(data, 'chat')
    except AttributeError:
        data=data
    first_name=data.first_name
    if not data.first_name:
        first_name=''
    last_name=data.last_name
    if not data.last_name:
        last_name=''
    username=data.username
    if not data.username:
        username=''
    defaults_dict={
        'first_name':first_name,
        'last_name':last_name,
        'username':username,
    }
    telegram_user,create_status=BotUser.objects.update_or_create(telegram_id=data.id,defaults=defaults_dict)
    if create_status is False:
        logger.info(f'Пользователь обновлен {first_name} {last_name} {username}')
    else:
        logger.info(f'Пользователь добавлен {first_name} {last_name} {username}')
    return create_status














