import telebot
from telebot import types # для указание типов
import config
import logging
import os
import json

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

bot = telebot.TeleBot(BOT_TOKEN)
CHANNEL_ID = '-1002034407496'
ADMIN_ID = 2091042930
USERS_FILE = 'users.txt'
HOROSCOPES_FILE = 'horoscopes.json'  # Изменен формат файла на JSON
ANGEL_NUMBERS_FILE = 'angel_numbers.json'  # Изменен формат файла на JSON
ZODIAC_SIGNS = ["♈Овен", "♉Телец", "♊Близнецы", "♋Рак", "♌Лев", "♍Дева", "♎Весы", "♏Скорпион", "♐Стрелец", "♑Козерог", "♒Водолей", "♓Рыбы"]

def load_angel_numbers():
    """Загружает ангельские числа из файла JSON."""
    angel_numbers = {}
    if os.path.exists(ANGEL_NUMBERS_FILE):
        try:
            with open(ANGEL_NUMBERS_FILE, 'r', encoding='utf-8') as f:
                angel_numbers = json.load(f)
        except Exception as e:
            logging.error(f"Ошибка при чтении файла ангельских чисел: {e}")
            angel_numbers = {}  # Если не удалось загрузить, инициализируем пустым словарем
    else:
        logging.warning(f"Файл ангельских чисел {ANGEL_NUMBERS_FILE} не найден.")
    return angel_numbers


def save_angel_numbers(angel_numbers):
    """Сохраняет ангельские числа в файл JSON."""
    try:
        with open(ANGEL_NUMBERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(angel_numbers, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при записи в файл ангельских чисел: {e}")

# Загружаем ангельские числа при старте бота
angel_numbers = load_angel_numbers()


# --- Функции для работы с файлом гороскопов ---
def load_horoscopes():
    """Загружает гороскопы из файла JSON."""
    horoscopes = {}
    if os.path.exists(HOROSCOPES_FILE):
        try:
            with open(HOROSCOPES_FILE, 'r', encoding='utf-8') as f:
                horoscopes = json.load(f)
        except Exception as e:
            logging.error(f"Ошибка при чтении файла гороскопов: {e}")
            horoscopes = {sign: f"Гороскоп для {sign} еще не обновлен." for sign in ZODIAC_SIGNS}
            save_horoscopes(horoscopes)
            return horoscopes
    else:
        horoscopes = {sign: f"Гороскоп для {sign} еще не обновлен." for sign in ZODIAC_SIGNS}
        save_horoscopes(horoscopes)

    return horoscopes


def save_horoscopes(horoscopes):
    """Сохраняет гороскопы в файл JSON."""
    try:
        with open(HOROSCOPES_FILE, 'w', encoding='utf-8') as f:
            json.dump(horoscopes, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при записи в файл гороскопов: {e}")


# Инициализация гороскопов при старте бота
horoscopes = load_horoscopes()





# --- Функции для работы с файлом пользователей ---
def load_users():
    users_data = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        user_id_str, zodiac_sign = line.strip().split(':', 1)
                        users_data[int(user_id_str)] = zodiac_sign
                    except ValueError:
                        logging.warning(f"Некорректная строка в файле пользователей: {line.strip()}")
        except Exception as e:
            logging.error(f"Ошибка при чтении файла пользователей: {e}")

    return users_data

def save_users(users_data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        for user_id, zodiac_sign in users_data.items():
            f.write(f"{user_id}:{zodiac_sign}\n")

# Инициализируем данные пользователей при запуске бота
user_data = load_users()

def is_subscribed(chat_id):
    try:
        user_status = bot.get_chat_member(CHANNEL_ID, chat_id).status
        return user_status in ("member", "administrator", "creator")
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False

def show_home_button(chat_id):
    """Отправляет клавиатуру с кнопкой 'Домой'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_home = types.KeyboardButton("⬅ Назад") #(Домой)
    markup.add(btn_home)
    return markup


def show_main_menu(chat_id):
    """Отправляет главное меню с кнопками "Гороскоп", "Матрица судьбы", "Ангельские числа" и "Задать вопрос"."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_horoscope = types.KeyboardButton("🔮 Гороскоп")
    #btn_matrix = types.KeyboardButton("✨ Матрица судьбы")
    btn_angel_numbers = types.KeyboardButton("😇 Ангельские числа")
    #btn_ask_question = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn_horoscope, btn_angel_numbers)
    #markup.add(btn_ask_question, btn_matrix)
    bot.send_message(chat_id, "Выберите интересующий вас раздел:", reply_markup=markup)

def show_zodiac_signs(chat_id):
    """Отправляет меню со знаками зодиака и кнопкой 'Домой'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = [types.KeyboardButton(sign) for sign in ZODIAC_SIGNS]
    markup.add(*btns)
    markup.add(types.KeyboardButton("⬅ Назад"))  # Добавляем кнопку "Домой"
    bot.send_photo(chat_id, photo='https://wallpapers.com/images/hd/cancer-zodiac-sign-1920-x-1080-603n4noypvpm7m0k.jpg',
                       caption="Выберите ваш знак зодиака", reply_markup=markup)



def show_angel_numbers_menu(chat_id):
    """Отправляет меню ангельских чисел с кнопкой 'Назад'."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton("⬅ Назад")
    markup.add(btn_back)
    bot.send_message(chat_id, "Что такое ангельские числа?\n\nАнгельские числа - это повторяющиеся последовательности чисел, которые, как считается, несут в себе послания от ангелов и духовных наставников. Каждое число имеет свое значение и может помочь вам понять текущую ситуацию в жизни, принять правильное решение или получить поддержку.", reply_markup=markup)
    bot.register_next_step_handler(bot.send_message(chat_id, "Пожалуйста, введите свою дату рождения в формате ДД.ММ.ГГГГ:"), get_birthdate)

def get_birthdate(message):
    """Получает дату рождения пользователя и вычисляет число ангела."""
    chat_id = message.chat.id
    birthdate = message.text
    try:
        # Проверяем формат даты
        day, month, year = map(int, birthdate.split('.'))
        if not (1 <= day <= 31 and 1 <= month <= 12 and 1000 <= year <= 2100):
            raise ValueError("Некорректный формат даты")

        # Вычисляем число ангела
        angel_number = calculate_angel_number(day, month, year)

        # Сохраняем дату рождения в user_data (вместе со знаком зодиака)
        zodiac_sign = user_data.get(chat_id, "Не определен")  # Получаем знак зодиака, если есть
        user_data[chat_id] = f"{zodiac_sign}:{birthdate}"  # Сохраняем и знак зодиака и дату
        save_users(user_data)

        # Выводим описание ангельского числа
        angel_number_str = str(angel_number)  # Преобразуем в строку для поиска
        if angel_number_str in angel_numbers:
            bot.send_message(chat_id, f"Ваше ангельское число: {angel_number}\n\n{angel_numbers[angel_number_str]}", reply_markup=show_home_button(chat_id))  # Ключ делаем строкой
        else:
            bot.send_message(chat_id, f"Ваше ангельское число: {angel_number}\n\nК сожалению, для этого числа пока нет описания.", reply_markup=show_home_button(chat_id))

    except ValueError as e:
        bot.send_message(chat_id, f"Ошибка: \nПожалуйста, введите дату рождения в формате ДД.ММ.ГГГГ:", reply_markup=show_home_button(chat_id))
        bot.register_next_step_handler(message, get_birthdate)  # Запрашиваем дату еще раз

def calculate_angel_number(day, month, year):
    """Вычисляет ангельское число."""
    total = day + month + year
    while total > 9:
        total = sum(map(int, str(total)))
    return total





@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if is_subscribed(chat_id):
        # Пользователь подписан, показываем главное меню
        show_main_menu(chat_id)
        if chat_id not in user_data:
            user_data[chat_id] = None
            save_users(user_data)
    else:
        # Пользователь не подписан, предлагаем подписаться
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_check_sub = types.KeyboardButton("✅ Я подписался")
        markup.add(btn_check_sub)

        bot.send_message(chat_id,
                             "Для использования бота необходимо подписаться на канал: " + f"https://t.me/+cgfnAiJiaTk2NjEy\n\n"
                             "Нажмите кнопку 'Я подписался' после подписки.",
                             reply_markup=markup)
        bot.register_next_step_handler(message, check_subscription)  # Передаём message, а не message_id


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if is_subscribed(chat_id):
        # Пользователь подписан, показываем главное меню
        show_main_menu(chat_id)
        if chat_id not in user_data:
            user_data[chat_id] = None
            save_users(user_data)
    else:
        # Пользователь не подписан, предлагаем подписаться
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_check_sub = types.KeyboardButton("✅ Я подписался")
        markup.add(btn_check_sub)

        bot.send_message(chat_id,
                             "Для использования бота необходимо подписаться на канал: " + f"https://t.me/+cgfnAiJiaTk2NjEy\n\n"
                             "Нажмите кнопку 'Я подписался' после подписки.",
                             reply_markup=markup)
        bot.register_next_step_handler(message, check_subscription)  # Передаём message, а не message_id


def check_subscription(message):  # Убрали message_id, так как не удаляем сообщение
    chat_id = message.chat.id

    if message.text == "✅ Я подписался":
        if is_subscribed(chat_id):
            # Пользователь подписался после нажатия кнопки
            show_main_menu(chat_id)
            if chat_id not in user_data:
                user_data[chat_id] = None
                save_users(user_data)
        else:
            # Пользователь нажал кнопку, но не подписался
            bot.send_message(chat_id, "Вы не подписались на канал")
            # Снова отправляем предложение подписаться
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_check_sub = types.KeyboardButton("✅ Я подписался")
            markup.add(btn_check_sub)

            bot.send_message(chat_id,
                                 "Для использования бота необходимо подписаться на канал: " + f"https://t.me/+cgfnAiJiaTk2NjEy\n\n"
                                 "Нажмите кнопку 'Я подписался' после подписки.",
                                 reply_markup=markup)
            bot.register_next_step_handler(message, check_subscription)
    else:
        # Пользователь ввел что-то другое
        bot.send_message(chat_id, "Пожалуйста, нажмите кнопку 'Я подписался'.")
        # Снова отправляем предложение подписаться
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_check_sub = types.KeyboardButton("✅ Я подписался")
        markup.add(btn_check_sub)

        bot.send_message(chat_id,
                             "Для использования бота необходимо подписаться на канал: " + f"https://t.me/+cgfnAiJiaTk2NjEy\n\n"
                             "Нажмите кнопку 'Я подписался' после подписки.",
                             reply_markup=markup)
        bot.register_next_step_handler(message, check_subscription)



def show_matrix_menu(chat_id):
    """Отправляет меню "Матрица судьбы" с кнопками "Рассчитать" и "Назад"."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_calculate = types.KeyboardButton("Рассчитать")
    btn_back = types.KeyboardButton("⬅ Назад")
    markup.add(btn_calculate, btn_back)
    bot.send_message(chat_id, "Что вы хотите сделать?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "✨ Матрица судьбы")
def matrix_sudby_handler(message):
    """Обрабатывает нажатие кнопки "Матрица судьбы"."""
    bot.send_message(message.chat.id,
                     "Матрица судьбы - это метод самопознания, основанный на 22 энергиях мироздания. Он позволяет узнать свои сильные и слабые стороны, предназначение, кармические уроки и многое другое.")
    show_matrix_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "😇 Ангельские числа")
def angel_numbers_handler(message):
    """Обрабатывает нажатие кнопки "Ангельские числа"."""
    show_angel_numbers_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "⬅ Назад" or message.text == "⬅ Назад")
def back_to_main_menu(message):
    """Возвращает пользователя в главное меню."""
    show_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "🔮 Гороскоп")
def horoscope_handler(message):
    """Обрабатывает нажатие кнопки "Гороскоп"."""
    show_zodiac_signs(message.chat.id)



# Словарь для хранения состояния редактирования гороскопа
admin_edit_state = {}


@bot.message_handler(commands=['set'])
def set_horoscope_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.InlineKeyboardMarkup()
    for sign in ZODIAC_SIGNS:
        markup.add(types.InlineKeyboardButton(sign, callback_data=f'set_sign:{sign}'))
    bot.send_message(message.chat.id, "Выберите знак зодиака для установки гороскопа:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_sign:'))
def set_sign_callback(call):
    sign = call.data.split(':')[1]
    admin_edit_state[call.from_user.id] = {'sign': sign, 'waiting_for_text': True}
    bot.send_message(call.message.chat.id, f"Теперь отправьте текст гороскопа для {sign}:")
    bot.answer_callback_query(call.id, text=f"Выбран знак: {sign}")


@bot.message_handler(commands=['angel'])
def set_angel_command(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.InlineKeyboardMarkup()
    for i in range(1, 10):  # Числа от 1 до 9
        markup.add(types.InlineKeyboardButton(str(i), callback_data=f'set_angel:{i}'))  # Ключ как строка
    bot.send_message(message.chat.id, "Выберите ангельское число для установки описания:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_angel:'))
def set_angel_callback(call):
    number = call.data.split(':')[1]
    admin_edit_state[call.from_user.id] = {'type': 'angel', 'target': number, 'waiting_for_text': True}  # Добавлено поле type
    bot.send_message(call.message.chat.id, f"Теперь отправьте текст описания для ангельского числа {number}:")
    bot.answer_callback_query(call.id, text=f"Выбрано ангельское число: {number}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def process_admin_input(message):
    user_id = message.from_user.id
    if user_id in admin_edit_state and admin_edit_state[user_id]['waiting_for_text']:
        text = message.text
        type = admin_edit_state[user_id]['type']
        target = admin_edit_state[user_id]['target']

        if type == 'horoscope':
            horoscopes[target] = text
            save_horoscopes(horoscopes)
            bot.reply_to(message, f"Гороскоп для {target} успешно обновлен.")
        elif type == 'angel':
            angel_numbers[target] = text  # target уже строка
            save_angel_numbers(angel_numbers)
            bot.reply_to(message, f"Описание для ангельского числа {target} успешно обновлено.")

        del admin_edit_state[user_id]



@bot.message_handler(content_types=['text'])
def func(message):
    if message.text in ZODIAC_SIGNS:
        user_data[message.chat.id] = message.text
        save_users(user_data)
        horoscope_text = horoscopes[message.text]
        bot.send_message(message.chat.id, horoscope_text, reply_markup=show_home_button(message.chat.id)) # Отправляем гороскоп и кнопку "Домой"
        return

    elif message.text == "Рассчитать":
        # TODO: Реализовать логику расчета матрицы судьбы
        bot.send_message(message.chat.id, "Функция расчета матрицы судьбы пока не реализована.")
    elif message.text == "❓ Задать вопрос":
        # TODO: Реализовать логику задания вопроса
        bot.send_message(message.chat.id, "Функция задания вопроса пока не реализована.")
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")




# Запуск бота
try:
    bot.polling(none_stop=True)
except Exception as e:
    logging.exception("Ошибка при запуске бота")
