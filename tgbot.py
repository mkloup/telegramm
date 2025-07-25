import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message, InputFile

TOKEN = '8169250972:AAG77MXmp_AY1t-RNzPuL1RQZ-I38JJU6qs'
bot = telebot.TeleBot(TOKEN)

admin_id = [1943575640]  # Твой Telegram ID
users_sent_id = set()    # Для отслеживания, кто уже отправил свой ID

# Список героев и скинов
heroes = {
    "Alucard": ["Demonic Blade", "Obsidian Blade"],
    "Layla": ["Blue Specter", "Bunny Babe"],
    "Gusion": ["Cyber Ops", "Night Owl"],
    "Miya": ["Captain Thorns", "Christmas Cheer"]
}

# Прайс обычных алмазов
diamonds = [
    "Алмазный пропуск - 770 тг",
    "86💎 - 660 тг",
    "172💎 - 1310 тг",
    "257💎 - 1900 тг",
    "343💎 - 2560 тг (для фазы)",
    "429💎 - 3210 тг",
    "514💎 - 3800 тг",
    "706💎 - 5150 тг",
    "792💎 - 5760 тг",
    "878💎 - 6400 тг",
    "963💎 - 6940 тг",
    "1412💎 - 10050 тг",
    "2195💎 - 15200 тг",
    "2452💎 - 17050 тг",
    "2901💎 - 20050 тг",
    "3685💎 - 24950 тг",
    "3942💎 - 26890 тг",
    "4391💎 - 29870 тг",
    "5532💎 - 36900 тг",
    "5789💎 - 38800 тг",
    "6238💎 - 41300 тг",
    "9288💎 - 60500 тг",
    "Сумеречный пропуск - 4300 тг"
]

# Прайс бонусных алмазов
bonus_diamonds = [
    "50+50💎 - 510 тг",
    "150+150💎 - 1380 тг",
    "250+250💎 - 2300 тг",
    "500+500💎 - 4660 тг"
]

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu.add(
    KeyboardButton('💎 Бонусные алмазы'),
    KeyboardButton('📄 Прайс-лист'),
    KeyboardButton('💎 Купить алмазы'),
    KeyboardButton('🤫 Скинчейнджер'),
    KeyboardButton('✉️ Отзывы'),
    KeyboardButton('✉️ Мой чат'),
    KeyboardButton('💜 Мой канал'),
    KeyboardButton('🔙 Назад')
)

# Команда /start
@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id
    if user_id not in users_sent_id:
        msg = bot.send_message(message.chat.id, "Приветик!🥰 Пожалуйста, пришли свой ID (в формате 1393879353 (15746)) для продолжения.")
        bot.register_next_step_handler(msg, get_user_id)
    else:
        bot.send_message(message.chat.id, "С возвращением! Выбери интересующий пункт меню:", reply_markup=main_menu)

# Обработка ввода ID
def get_user_id(message: Message):
    user_input = message.text
    user_id = message.from_user.id
    users_sent_id.add(user_id)

    for admin in admin_id:
        bot.send_message(admin, f"🆕 Новый пользователь отправил ID:\n{user_input}\nTelegram ID: {user_id}")

    bot.send_message(message.chat.id, "Спасибо! Теперь выбери пункт меню:", reply_markup=main_menu)

# Отправка прайса
def send_diamond_price_list(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in diamonds:
        markup.add(KeyboardButton(f"💎 {item}"))
    markup.add(KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите количество алмазов:", reply_markup=markup)

# Отправка бонусных алмазов
def send_bonus_diamonds(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for item in bonus_diamonds:
        markup.add(KeyboardButton(f"💎 {item}"))
    markup.add(KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "💎 Бонусные алмазы (только при первом пополнении, с х2 бонусом):", reply_markup=markup)

# Обработка кнопок
@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    text = message.text

    if text == '📄 Прайс-лист' or text == '💎 Купить алмазы':
        send_diamond_price_list(message)

    elif text == '💎 Бонусные алмазы':
        send_bonus_diamonds(message)

    elif text.startswith("💎 ") and any(text.startswith(f"💎 {d.split(' - ')[0]}") for d in diamonds + bonus_diamonds):
        bot.send_message(message.chat.id, "💳 Оплата на карту: *4400 4302 1635 1269*\n\nОтправьте PDF-файл чека. После подтверждения админ отправит вам алмазы в течение часа. Работаем с 10:00 до 24:00. По вопросам: @zadrotzxc", parse_mode='Markdown')

    elif text == '🤫 Скинчейнджер':
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for hero in heroes:
            markup.add(KeyboardButton(hero))
        markup.add(KeyboardButton('🔙 Назад'))
        bot.send_message(message.chat.id, "Выберите героя:", reply_markup=markup)

    elif text in heroes:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for skin in heroes[text]:
            markup.add(KeyboardButton(skin))
        markup.add(KeyboardButton('🔙 Назад'))
        bot.send_message(message.chat.id, f"Какой скин для {text} вас интересует? За каждый скин — 100 тг", reply_markup=markup)

    elif any(text in skins for skins in heroes.values()):
        bot.send_message(message.chat.id, "💳 Оплата на карту: *4400 4302 1635 1269*\n\nОтправьте PDF-файл оплаты. После проверки вы получите файл с скином и инструкцию по установке (YouTube-ссылка).", parse_mode='Markdown')

    elif text == '✉️ Мой чат':
        bot.send_message(message.chat.id, "Вот ссылка на чат: https://t.me/+g1PG1UEztuw5NmUy")

    elif text == '💜 Мой канал':
        bot.send_message(message.chat.id, "Вот ссылка на канал: https://t.me/+5vLdcOTA8BhkN2Y6")

    elif text == '✉️ Отзывы':
        bot.send_message(message.chat.id, "Отзывы можно посмотреть здесь: https://t.me/DiamondsMahito")

    elif text == '🔙 Назад':
        start(message)

    else:
        bot.send_message(message.chat.id, "Пожалуйста, выбери вариант из меню.")

# Обработка PDF-файлов
@bot.message_handler(content_types=['document'])
def handle_pdf(message: Message):
    if message.document.mime_type == 'application/pdf':
        for admin in admin_id:
            bot.forward_message(admin, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Файл получен! Ожидайте подтверждение от администратора в течение часа.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте именно PDF-файл.")

# Запуск бота
bot.polling(none_stop=True)
