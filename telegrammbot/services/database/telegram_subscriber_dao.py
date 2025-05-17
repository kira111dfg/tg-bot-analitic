import logging
from datetime import timezone, datetime

from asgiref.sync import sync_to_async
from telebot.types import Chat,User

from services.database.telegram_chat_dao import get_telegram_chat_by_chat_id
from tgbot.models import TelegramSubscriber, TelegramChat, InviteLink

logger = logging.getLogger(__name__)
async def update_or_create_subscriber(chat_data:Chat,user_data:User,subscribed:bool,invite_link:InviteLink|None):
    telegram_chat=await get_telegram_chat_by_chat_id(telegram_chat_id=chat_data.id)
    defaults_dict={
        'telegram_chat':telegram_chat,
        'username': user_data.username,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'subscribed':subscribed,
    }
    if subscribed is True:
        defaults_dict['datetime_subscribed']=datetime.now()
    else:
        defaults_dict['datetime_unsubscribed'] = datetime.now()
    if invite_link:
        telegram_subscriber,create_status=await TelegramSubscriber.objects.aupdate_or_create(invite_link=invite_link,telegram_id=user_data.id,
                                                                                             defaults=defaults_dict,
                                                                                       )
    else:
        telegram_subscriber,create_status = await TelegramSubscriber.objects.aupdate_or_create(telegram_chat=telegram_chat,telegram_id=user_data.id,
                                                                                         defaults=defaults_dict)
    return telegram_subscriber

async def check_exist_subscriber_in_channel(chat_data:Chat,user_data:User)->bool:
    telegram_chat=await get_telegram_chat_by_chat_id(telegram_chat_id=chat_data.id)
    if telegram_chat is None:
        return False
    try:
        await TelegramSubscriber.objects.aget(telegram_chat=telegram_chat,telegram_id=user_data.id)
    except TelegramSubscriber.DoesNotExist as err:
        logger.warning(f'Не найден подписчик в канале {chat_data.title} {err}')
        return False
    return True


















