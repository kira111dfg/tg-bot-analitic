
from django.db import models
from django.utils.translation import gettext as _

class BotUser(models.Model):
    telegram_id = models.PositiveBigIntegerField(_('ID Telegram'),blank=True, null=True,unique=True,db_index=True)

    username = models.CharField(_('Юзернейм'),max_length=150,blank=True,null=True)
    first_name = models.CharField(_('Имя'),max_length=150,blank=True,null=True)
    last_name = models.CharField(_('Фамилия'),max_length=150,blank=True,null=True)

    class Meta:
        verbose_name = _('Пользователь бота')
        verbose_name_plural = _('Пользователи бота')



class TelegramChat(models.Model):
    name = models.CharField(_('Имя канала'), max_length=150, blank=True, null=True)
    #bot_user=models.ForeignKey(BotUser, verbose_name=_('Пользователь бота'), on_delete=models.CASCADE)
    chat_id = models.BigIntegerField(_('ID Канала'))
    username = models.CharField(_('Username канала'), max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = _('Канал')
        verbose_name_plural = _('Каналы')



class InviteLink(models.Model):
    telegram_chat = models.ForeignKey(TelegramChat, verbose_name=_('Телеграм канал'), on_delete=models.CASCADE)

    creates_join_request=models.BooleanField(_('Запрос на добавление'),default=False)
    link=models.CharField(_('Ссылка'), max_length=150, blank=True, null=True)
    is_revoked=models.BooleanField(_('is revoked'),default=False)
    name=models.CharField(_('Имя ссылки'), max_length=150, blank=True, null=True)
    creator_full_name=models.CharField(_('Создатель name'), max_length=250, blank=True, null=True)
    creator_id = models.CharField(_('Создатель id'), max_length=250, blank=True, null=True)
    creator_username = models.CharField(_('Создатель username'), max_length=250, blank=True, null=True)
    expire_date=models.CharField(_('Время истечения'), max_length=150, blank=True, null=True)
    member_limit=models.IntegerField(_('Лимит подписок'), blank=True, null=True)
    is_primary=models.BooleanField(_('is primary'),default=False)
    pending_join_request_count=models.IntegerField(_('pending_join_request_count'), blank=True, null=True)

    public_link=models.BooleanField(_('Публичная ссылка'),default=False)
    notification=models.BooleanField(_('Уведомление о подписках'),default=False)

    class Meta:
        verbose_name = _('Пригласительная ссылка')
        verbose_name_plural = _('Пригласительные ссылки')

class TelegramSubscriber(models.Model):
    telegram_id = models.PositiveBigIntegerField(_('ID Telegram'), blank=True, null=True,  db_index=True)
    invite_link=models.ForeignKey(InviteLink,verbose_name=_('Пригласительная ссылка'),on_delete=models.CASCADE)
    telegram_chat = models.ForeignKey(TelegramChat, verbose_name=_('Телеграм канал'), on_delete=models.CASCADE)
    username = models.CharField(_('Юзернейм'), max_length=150, blank=True, null=True)
    first_name = models.CharField(_('Имя'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=150, blank=True, null=True)
    subscribed=models.BooleanField(_('Подписан'), default=False)
    datetime_subscribed=models.DateTimeField(_('Время подписки'), blank=True, null=True)
    datetime_unsubscribed = models.DateTimeField(_('Время отписки'), blank=True, null=True)

    class Meta:
        verbose_name = _('Подписчик')
        verbose_name_plural = _('Подписчики')