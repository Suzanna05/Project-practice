# Телеграм бот на Python

Несложный телеграм бот планировщик, который запоминает все задачи. Можно попросить посмотреть все 
ваши дела на определеный день, которые вы запланировали заранее.

---

## Поддерживаемые команды:

### Встроенные команды:

- `/start` - показать главное меню
- `/data` - посмотреть задачи на дату
- `/done` - отметить выполненную задачу
- `/results` - статистика выполненных задач
- `/help` - справка


## Встроенные кнопки:

- `Добавить задачу` — Добавление задачи на определенный день.  
- `Отметить выполненное` — Отмечает задачу выполненной.
- `Моя статистика` — Показывает сколько всего выполненых задач есть. 
- `Мои задачи` — Показывает все задачи вписанные в бот. 
- `Помощь` — Показывает все функции бота.

---

# Отчет по созданию Telegram бота для управления расписанием

## Цели и задачи:
1. Базовое изучение Python и библиотеки `telebot` для работы с Telegram API.
2. Создание функционального бота для управления задачами и расписанием.
3. Реализация интерактивного взаимодействия с пользователем через кнопки и команды.
4. Организация хранения и обработки данных задач.

---

## Задачи, выполненные в процессе:

### 1. Настройка окружения
- Установка Python и необходимых библиотек (`pyTelegramBotAPI`).
- Создание бота через BotFather в Telegram и получение токена.

### 2. Создание базовой структуры бота
- Инициализация бота с использованием токена.
- Настройка хранилища для данных пользователей и задач:
  ```python
  user_data = {}
  tasks = {}

### 3. Главное меню
-Создание интерактивной клавиатуры:

 ```python
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
```

### 4. Обработка команд
-Реализация основных команд бота:

 ```python
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """
Привет! Я бот для управления расписанием.
Доступные команды:
/start - главное меню
/data - просмотр задач
/done - отметить выполнение
/results - статистика
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_menu())
```

### 5. Добавление задач
-Пошаговый процесс добавления:

 ```python
@bot.message_handler(func=lambda message: message.text == "Добавить задачу")
def add_task_command(message):
    bot.send_message(message.chat.id, "Введите дату (ДД.ММ.ГГГГ):")
    user_data[message.chat.id] = {"step": "waiting_date"}

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "waiting_date")
def get_date(message):
    if validate_date(message.text):
        user_data[message.chat.id] = {
            "step": "waiting_task", 
            "date": message.text
        }
        bot.send_message(message.chat.id, "Введите название задачи:")
```

### 6. Просмотр и отметка задач
-Функционал работы с задачами:

 ```python
@bot.message_handler(func=lambda message: message.text == "Мои задачи")
def show_tasks(message):
    date = # получение даты из user_data
    if date in tasks:
        task_list = "\n".join([
            f"{i+1}. {t['time']} - {t['task']}" 
            for i,t in enumerate(tasks[date])
        ])
        bot.send_message(message.chat.id, f"Задачи на {date}:\n{task_list}")

@bot.message_handler(func=lambda message: message.text == "Отметить выполненное")
def mark_done(message):
    # Логика отметки выполнения
    task["done"] = True
    bot.send_message(message.chat.id, "Задача отмечена выполненной!")
```
### 7. Валидация данных
-Проверка вводимых данных:
 ```python
def validate_date(date):
    try:
        day, month, year = map(int, date.split('.'))
        return 1 <= day <= 31 and 1 <= month <= 12
    except:
        return False

def validate_time(time):
    try:
        start, end = time.split('-')
        return all(0 <= int(x) < 24 for x in start.split(':'))
    except:
        return False
```
### 8. Запуск бота
-Основной цикл работы:
 ```python
if __name__ == '__main__':
    bot.polling(none_stop=True)
```
## Итоги
### Реализован функциональный бот с:
-Добавлением и просмотром задач

-Отметкой выполнения

-Валидацией ввода

-Удобным интерактивным меню
