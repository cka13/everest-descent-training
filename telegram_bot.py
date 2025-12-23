#!/usr/bin/env python3
"""
Telegram бот для Everest Descent Training
Отвечает на сообщения пользователей и предоставляет информацию о курсах.

Установка:
pip install python-telegram-bot

Запуск:
python telegram_bot.py
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8186974891:AAGc3TAdirnE0WB0mMDyPOTiCelKNSxhUuw"
ADMIN_CHAT_ID = "132310665"  # Ваш Chat ID для получения заявок

# ===== ТЕКСТЫ =====
WELCOME_MESSAGE = """
🏔️ *Добро пожаловать в Everest Descent Training!*

Мы — единственная в России программа подготовки к экстремальному спуску с Эвереста.

*Что мы предлагаем:*
• 11 недель интенсивной подготовки
• Методика мирового рекордсмена Анджея Баргиэля
• 100% безопасность за 11 лет работы
• 50+ успешных выпускников

Выберите интересующий вас раздел:
"""

COURSES_MESSAGE = """
📚 *Наши курсы:*

*1. Базовый курс — 175,000 ₽*
• 6 недель обучения
• Групповые занятия (до 6 чел)
• Практика на Эльбрусе
• Оборудование включено

*2. Профессиональный курс — 350,000 ₽* ⭐
• 11 недель полной программы
• Мини-группы (до 4 чел)
• Практика в Непале
• Международный сертификат

*3. VIP: Экспедиция на Эверест — 750,000 ₽*
• Полная программа + экспедиция
• Персональный инструктор
• Реальный спуск с Эвереста
• Документальный фильм о вас

💳 Рассрочка 0% на 12 месяцев
🔄 Гарантия возврата 100% в первые 14 дней
"""

CONTACT_MESSAGE = """
📞 *Как с нами связаться:*

📱 Телефон: +7 (999) 123-45-67
📧 Email: info@everestdescent.ru
🌐 Сайт: https://cka13.github.io/everest-descent-training/

🏠 Адрес: Москва, ул. Альпинистов, 15

Хотите записаться на *бесплатную консультацию*?
Нажмите кнопку ниже! 👇
"""

FAQ_MESSAGE = """
❓ *Частые вопросы:*

*Нужен ли опыт в альпинизме?*
Нет! Мы принимаем новичков. Главное — хорошая физическая форма.

*Насколько это опасно?*
За 11 лет — ни одного серьёзного инцидента. Врач и спасательная команда на каждом этапе.

*Можно ли в рассрочку?*
Да! Рассрочка 0% на 12 месяцев.

*Что если передумаю?*
100% возврат в первые 14 дней без вопросов.

*Когда ближайший набор?*
Набор на сезон 2025 открыт! Осталось 4 места.
"""

# ===== КЛАВИАТУРЫ =====
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Курсы и цены", callback_data="courses")],
        [InlineKeyboardButton("❓ Частые вопросы", callback_data="faq")],
        [InlineKeyboardButton("📞 Контакты", callback_data="contact")],
        [InlineKeyboardButton("✍️ Записаться на консультацию", callback_data="signup")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_signup_keyboard():
    keyboard = [
        [InlineKeyboardButton("✍️ Записаться", callback_data="signup")],
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== ОБРАБОТЧИКИ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
*Команды бота:*

/start — Главное меню
/courses — Курсы и цены
/faq — Частые вопросы
/contact — Контакты
/signup — Записаться на консультацию

Или просто напишите ваш вопрос — мы ответим!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def courses_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /courses"""
    await update.message.reply_text(
        COURSES_MESSAGE,
        parse_mode='Markdown',
        reply_markup=get_signup_keyboard()
    )

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /faq"""
    await update.message.reply_text(
        FAQ_MESSAGE,
        parse_mode='Markdown',
        reply_markup=get_back_keyboard()
    )

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /contact"""
    await update.message.reply_text(
        CONTACT_MESSAGE,
        parse_mode='Markdown',
        reply_markup=get_signup_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(
            WELCOME_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
    elif query.data == "courses":
        await query.edit_message_text(
            COURSES_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_signup_keyboard()
        )
    elif query.data == "faq":
        await query.edit_message_text(
            FAQ_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_back_keyboard()
        )
    elif query.data == "contact":
        await query.edit_message_text(
            CONTACT_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_signup_keyboard()
        )
    elif query.data == "signup":
        signup_text = """
✍️ *Записаться на бесплатную консультацию*

Отправьте одним сообщением:
• Ваше имя
• Телефон для связи
• Какой курс интересует

Пример:
_Иван Петров, +7 999 123-45-67, Профессиональный курс_

Мы перезвоним в течение 2 часов!
        """
        await query.edit_message_text(
            signup_text,
            parse_mode='Markdown',
            reply_markup=get_back_keyboard()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    user = update.effective_user
    message_text = update.message.text
    
    # Пересылаем сообщение администратору
    admin_message = f"""
📨 *Новое сообщение от пользователя:*

👤 Имя: {user.first_name} {user.last_name or ''}
📱 Username: @{user.username or 'нет'}
🆔 ID: {user.id}

💬 Сообщение:
{message_text}
    """
    
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error sending to admin: {e}")
    
    # Отвечаем пользователю
    response = """
✅ *Спасибо за ваше сообщение!*

Мы получили вашу заявку и свяжемся с вами в ближайшее время.

⏰ Обычно мы отвечаем в течение 2 часов в рабочее время (10:00 - 20:00 МСК).

А пока вы можете:
    """
    
    await update.message.reply_text(
        response,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")

def main() -> None:
    """Запуск бота"""
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("courses", courses_command))
    application.add_handler(CommandHandler("faq", faq_command))
    application.add_handler(CommandHandler("contact", contact_command))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()





