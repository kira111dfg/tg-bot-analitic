

from telebot import BaseMiddleware

from services.database.bot_user_dao import update_or_create_tg_user


class MyMiddleware(BaseMiddleware):
    def __init__(self):
        super(MyMiddleware,self).__init__()
        self.update_sensitive=True
        self.update_types=['message']

    async def pre_process_message(self,message,data):
        my_data=None
        try:
            my_data=getattr(message,'chat')
        except AttributeError:
            pass
        try:
            my_data=getattr(message,'from_user')
        except AttributeError:
            pass
        if not my_data:
            return None
        if not message.text:
            return None
        await update_or_create_tg_user(my_data)

    async def post_process_message(self,message,data,exception):
        pass

    async def pre_process_edited_message(self,message,data):
        pass

    async def post_process_edited_message(self,message,data,exception):
        pass


