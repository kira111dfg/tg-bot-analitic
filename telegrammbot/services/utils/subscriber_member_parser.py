import logging
from telebot.types import ChatMemberUpdated
logger = logging.getLogger(__name__)

def member_is_subscribed(chat_member_updated:ChatMemberUpdated)->bool|None:
    status=chat_member_updated.difference.get('status')
    current_subscriber_status=status[1]
    if current_subscriber_status=='creator':
        return True
    elif current_subscriber_status=='left':
        return False
    logger.warning('Статус подписки не определен')
    return None