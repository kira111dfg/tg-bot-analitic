from django.contrib import admin

from tgbot.models import TelegramChat, BotUser, TelegramSubscriber, InviteLink
from django.contrib.auth.models import User,Group

admin.site.unregister(User)
admin.site.unregister(Group)
# Register your models here.
admin.site.register(TelegramChat)
admin.site.register(BotUser)
admin.site.register(TelegramSubscriber)
admin.site.register(InviteLink)