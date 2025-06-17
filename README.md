# Telegram Subscribe Tracker Bot 📲

Этот бот отслеживает, когда пользователь **подписывается** или **отписывается** от канала. Информация сохраняется в базу данных с точным временем события.

 Стек технологий

- Python 3.10+
- Django 
- Telegram Bot API 
- SQLite



Возможности

- Отслеживание события подписки (`chat_member`)
- Отслеживание отписки/удаления из канала
- Сохранение времени подписки и отписки в базу данных
- Админ-панель 


Установка

Клонируй проект
   ```bash
   git clone https://github.com/kira111dfg/tg-bot-analitic.git
   cd telegrammbot
Создай виртуальное окружение и установи зависимости
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
cоздай .env файл на основе шаблона
  TELEGRAM_BOT_TOKEN=your_bot_token
  DJANGO_SECRET_KEY=your_django_secret
Запусти миграции и сервер
  python manage.py migrate
  python manage.py runserver
Запусти бота
  python bot.py

