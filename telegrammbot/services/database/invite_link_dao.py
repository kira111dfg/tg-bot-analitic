import logging

from asgiref.sync import sync_to_async
from telebot.types import ChatInviteLink

from tgbot.models import InviteLink, TelegramChat
logger = logging.getLogger(__name__)


async def update_invite_link(telegram_chat:TelegramChat,link_data:ChatInviteLink):
    defaults_dict={
    'telegram_chat':telegram_chat,
    'creates_join_request':link_data.creates_join_request,
    'is_revoked':link_data.is_revoked,
    'name' :link_data.name,
    'creator_full_name':link_data.creator.full_name,
    'creator_id': link_data.creator.id,
    'creator_username': link_data.creator.username,
    'expire_date' :link_data.expire_date,
    'member_limit' :link_data.member_limit,
    'is_primary' :link_data.is_primary,
    'pending_join_request_count' :link_data.pending_join_request_count,
    }
    invite_link,create_status=await InviteLink.objects.aupdate_or_create(telegram_chat=telegram_chat,
                                                                    link=link_data.invite_link,
                                                                    defaults=defaults_dict)
    return invite_link,create_status


async def create_public_link(telegram_chat:TelegramChat,chat_username:str|None):
    link=None
    if chat_username:
        link=f'https://t.me/{chat_username}'
    try:
        invite_link=await InviteLink.objects.aget(telegram_chat=telegram_chat,public_link=True)
    except InviteLink.DoesNotExist:
        logger.info('Не нашел ссылку')
        invite_link=await InviteLink.objects.acreate(telegram_chat=telegram_chat,link=link,public_link=True)
        return invite_link
    return invite_link















