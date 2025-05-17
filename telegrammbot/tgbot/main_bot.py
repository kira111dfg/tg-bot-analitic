import logging

from telebot.async_telebot import AsyncTeleBot
import telebot
from django.conf import settings

from services.database.telegram_subscriber_dao import check_exist_subscriber_in_channel, update_or_create_subscriber
from services.utils.subscriber_member_parser import member_is_subscribed
from services.database.invite_link_dao import update_invite_link, create_public_link
from services.database.telegram_chat_dao import update_telegram_chat, get_all_channels
from .middleware import MyMiddleware
from telebot.types import ChatMemberUpdated
bot = AsyncTeleBot(settings.TOKEN_BOT,parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

bot.setup_middleware(MyMiddleware())

C=[-1002664391232,-1002359330141]

@bot.chat_member_handler()
async def chat_member_handler_bot(message:ChatMemberUpdated):
    #channels_ids=[channel.chat_id async for channel in await get_all_channels()]
    if message.chat.id not in C:
        return None
    telegram_chat=await update_telegram_chat(chat_data=message.chat)
    status=message.difference.get('status')
    invite_link=message.invite_link
    full_name=message.from_user.full_name
    username=message.from_user.username
    id=message.from_user.id
    invite_link_name=None
    invite_link_url=None
    try:
        invite_link_name=getattr(invite_link,'name')
        invite_link_url=getattr(invite_link,'invite_link')
    except AttributeError as err:
        logger.info(f'Не получил пригласительную ссылку:{err}')
        invite_link_db=await create_public_link(telegram_chat=telegram_chat,chat_username=message.chat.username)
    else:
        invite_link_db,create_status=await update_invite_link(telegram_chat=telegram_chat,link_data=message.invite_link)

    subscribed=member_is_subscribed(chat_member_updated=message)
    subscriber_exist=await check_exist_subscriber_in_channel(chat_data=message.chat,
                                                             user_data=message.from_user)

    if subscriber_exist is True:
        await update_or_create_subscriber(chat_data=message.chat,
                                          user_data=message.from_user,
                                          subscribed=subscribed,
                                          invite_link=None)
    else:
        await update_or_create_subscriber(chat_data=message.chat,
                                          user_data=message.from_user,
                                          subscribed=subscribed,
                                          invite_link=invite_link_db)

    if subscribed is True:
        status_text='❤️Подписались'
    elif subscribed is False:
        status_text='😡Отписались'
    else:
        status_text='🤪Неизвестно'
    text_message=(f'Канал:{telegram_chat.name}\n'
                  f'Статус:{status_text}\n'
                  f'Имя: {full_name}\n'
                  f'ID: {id}\n')
    if username:
        text_message += f'\n<b>Никнейм:</b>{username}'
    if invite_link_name:
        text_message += f'\nПригласительная ссылка:{invite_link_name}'
    if invite_link_url:
        text_message += f'\n<b>URL:</b>{invite_link_url}'
    await bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,text=text_message)
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет'
    await bot.send_message(message.chat.id, text)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)