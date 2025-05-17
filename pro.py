import telebot
from telebot import types

bot = telebot.TeleBot("7385196322:AAFa559F9t9zYJ5yrZu4LvC-k74iZx_BEuY")  # Замените на ваш токен

# Хранение данных
user_data = {}
tasks = {}

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "Добавить задачу",
        "Мои задачи",
        "Отметить выполненное",
        "Моя статистика",
        "Помощь"
    ]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"""
Привет, {user_name}! Я бот для управления расписанием.

Доступные команды:
/start - показать главное меню
/data - посмотреть задачи на дату
/done - отметить выполненную задачу
/results - статистика выполненных задач
/help - справка

Форматы ввода:
Дата - ДД.ММ.ГГГГ
Время - ЧЧ:ММ-ЧЧ:ММ
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == "Добавить задачу")
def add_task_command(message):
    start(message)

@bot.message_handler(func=lambda message: message.text == "Мои задачи")
def show_tasks_command(message):
    show_data(message)

@bot.message_handler(func=lambda message: message.text == "Отметить выполненное")
def mark_done_command(message):
    done(message)

@bot.message_handler(func=lambda message: message.text == "Моя статистика")
def show_stats_command(message):
    results(message)

@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_command(message):
    send_welcome(message)

@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {user_name}, начнем работать над твоим расписанием\nВведи дату (в виде ДД.ММ.ГГГГ):")
    user_data[message.chat.id] = {"step": "waiting_date"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_date")
def get_date(message):
    if not validate_date(message.text):
        bot.send_message(message.chat.id, "Некорректный формат даты. Введите дату в виде ДД.ММ.ГГГГ:")
        return
    
    user_data[message.chat.id] = {
        "step": "waiting_task",
        "date": message.text
    }
    bot.send_message(message.chat.id, "Записал. А теперь введи название дела:")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_task")
def get_task(message):
    user_data[message.chat.id].update({
        "step": "waiting_time",
        "task": message.text
    })
    bot.send_message(message.chat.id, "Хорошо. Напиши временные рамки (в виде ЧЧ:ММ-ЧЧ:ММ):")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_time")
def get_time(message):
    if not validate_time(message.text):
        bot.send_message(message.chat.id, "Некорректный формат времени. Введите в виде ЧЧ:ММ-ЧЧ:ММ:")
        return
    
    date = user_data[message.chat.id]["date"]
    task = user_data[message.chat.id]["task"]
    time = message.text
    
    if date not in tasks:
        tasks[date] = []
    tasks[date].append({"task": task, "time": time, "done": False})
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Главное меню", "Добавить ещё задачу")
    
    bot.send_message(message.chat.id, f"✅ Задача добавлена на {date}:\n🕒 {time}\n📝 {task}", reply_markup=markup)
    user_data[message.chat.id] = {}

@bot.message_handler(commands=['data'])
def show_data(message):
    bot.send_message(message.chat.id, "Введите дату, которая Вас интересует (в виде ДД.ММ.ГГГГ):")
    user_data[message.chat.id] = {"step": "waiting_data_date"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_data_date")
def process_data_date(message):
    date = message.text
    if date not in tasks or not tasks[date]:
        bot.send_message(message.chat.id, f"На {date} задач нет.", reply_markup=create_main_menu())
    else:
        task_list = "\n".join([f"🕒 {task['time']} - {task['task']}{' ✅' if task['done'] else ''}" for task in tasks[date]])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Главное меню", "Отметить выполненное")
        bot.send_message(message.chat.id, f"📅 Ваши задачи на {date}:\n{task_list}", reply_markup=markup)
    user_data[message.chat.id] = {}

@bot.message_handler(commands=['done'])
def done(message):
    bot.send_message(message.chat.id, "Введите дату, которая Вас интересует (в виде ДД.ММ.ГГГГ):")
    user_data[message.chat.id] = {"step": "waiting_done_date"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_done_date")
def process_done_date(message):
    date = message.text
    if date not in tasks or not tasks[date]:
        bot.send_message(message.chat.id, f"На {date} задач нет.", reply_markup=create_main_menu())
    else:
        undone_tasks = [task for task in tasks[date] if not task["done"]]
        if not undone_tasks:
            bot.send_message(message.chat.id, f"На {date} все задачи уже выполнены!", reply_markup=create_main_menu())
            return
            
        task_list = "\n".join([f"{i+1}. {task['time']} - {task['task']}" for i, task in enumerate(undone_tasks)])
        user_data[message.chat.id] = {
            "step": "waiting_task_number",
            "date": date,
            "undone_tasks": undone_tasks
        }
        bot.send_message(message.chat.id, f"📅 Невыполненные задачи на {date}:\n{task_list}\nВведите номер задачи, которую выполнили:")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_task_number")
def process_task_number(message):
    try:
        task_num = int(message.text) - 1
        date = user_data[message.chat.id]["date"]
        undone_tasks = user_data[message.chat.id]["undone_tasks"]
        
        if 0 <= task_num < len(undone_tasks):
            task_name = undone_tasks[task_num]["task"]
            # Находим эту задачу в основном списке и отмечаем выполненной
            for task in tasks[date]:
                if task["task"] == task_name and not task["done"]:
                    task["done"] = True
                    break
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Главное меню", "Отметить ещё задачу")
            
            bot.send_message(message.chat.id, f"✅ Готово, \"{task_name}\" — выполнено", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Неверный номер задачи.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите номер задачи.")
    finally:
        user_data[message.chat.id] = {}

@bot.message_handler(commands=['results'])
def results(message):
    done_count = sum(1 for date in tasks for task in tasks[date] if task["done"])
    bot.send_message(message.chat.id, f"🎉 Всего вы выполнили {done_count} задач. Ты молодец!", reply_markup=create_main_menu())

def validate_date(date):
    try:
        day, month, year = map(int, date.split('.'))
        return 1 <= day <= 31 and 1 <= month <= 12 and year >= 2023
    except:
        return False

def validate_time(time):
    try:
        start, end = time.split('-')
        start_h, start_m = map(int, start.split(':'))
        end_h, end_m = map(int, end.split(':'))
        return (0 <= start_h < 24 and 0 <= start_m < 60 and 
                0 <= end_h < 24 and 0 <= end_m < 60)
    except:
        return False

@bot.message_handler(func=lambda message: message.text == "Главное меню")
def return_to_main_menu(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text == "Добавить ещё задачу")
def add_another_task(message):
    start(message)

bot.polling(none_stop=True)