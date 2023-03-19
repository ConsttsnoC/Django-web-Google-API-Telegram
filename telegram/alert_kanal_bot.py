chat_id = 'ID-ЧАТА'
from telegram.ext import Updater, CommandHandler
from datetime import date, timedelta
import psycopg2
import schedule
import time
import telegram



# Определяем функцию start(), которая отправляет приветственное сообщение пользователю
def start(update, context):
    """
        Функция для обработки команды /start.
        Отправляет приветственное сообщение пользователю.
    """
    context.bot.send_message(chat_id=update.message.chat_id, text="Привет! Я буду каждый день присылать вам список просроченных поставок. И отдельно те, которые были просроченны вчера! Если вам нужно получить список введите команду /order ")

# Создаем объект Updater и привязываем его к Telegram боту
updater = Updater(token='5912200140:AAGPyK-PoMAwPVEaAKKNBC_-6YhX79AbzD0', use_context=True)

# Получаем диспетчер для регистрации обработчиков
dispatcher = updater.dispatcher

# Добавляем обработчик для команды /start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Функция order() проверяет просроченные заказы и отправляет уведомленияC:\test_Kanalservis\app_root
def order(update, context):
    """
       Функция для обработки команды /order.
       Проверяет просроченные заказы в базе данных и отправляет уведомления пользователю.
    """
    # Получаем дату вчерашнего дня и дату 30 дней назад
    yesterday = date.today() - timedelta(days=1)
    thirty_days_ago = date.today() - timedelta(days=30)

    # Подключаемся к базе данных
    conn = psycopg2.connect(
        database="НАЗВАНИЕ БД",
        user="ИМЯ ПОЛЬЗОВАТЕЛЯ",
        password="ПАРОЛЬ",
        port="5432"
    )
    cur = conn.cursor()

    # Выполняем запрос, чтобы получить просроченный заказ от вчерашнего дня
    cur.execute("SELECT order_number FROM my_table WHERE date = %s", (yesterday,))
    expired_order = cur.fetchone()

    # Отправляем сообщение пользователю, если есть просроченные заказы за последние 30 дней
    cur.execute("SELECT order_number, date FROM my_table WHERE date >= %s AND date < %s", (thirty_days_ago, date.today()))
    expired_orders = cur.fetchall()

    # Закрываем соединение с базой данных
    cur.close()
    conn.close()

    # Send a message to the user if there is an expired order from yesterday
    if expired_order:
        message = f"Order {expired_order[0]} is overdue! Please contact the customer."
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"За {yesterday.strftime('%Y-%m-%d')} нет просроченных поставок.")

    # Send a message to the user if there are expired orders within the last 30 days
    if expired_orders:
        message = "Все просроченные поставки за последние 30 дней\n"
        for order in expired_orders:
            message += f"- {order[0]} (Срок поставки: {order[1].strftime('%Y-%m-%d')})\n"
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Нет просроченных поставок за последние 30 дней.")

# Создаем объект бота Telegram и токен
bot = telegram.Bot(token='5912200140:AAGPyK-PoMAwPVEaAKKNBC_-6YhX79AbzD0')

def send_order_message_at_time(bot, chat_id, send_time):
    """
       Функция для отправки сообщений о просроченных заказах в заданное время.

       :param bot: объект бота Telegram
       :param chat_id: идентификатор чата
       :param send_time: время, когда нужно отправить сообщения о просроченных заказах
    """

    # Функция для получения списка просроченных заказов
    def order():
        """
            Функция для получения списка просроченных заказов из базы данных и отправки сообщений пользователю.
        """
        # Получаем дату вчерашнего дня и дату 30 дней назад от текущей даты
        yesterday = date.today() - timedelta(days=1)
        thirty_days_ago = date.today() - timedelta(days=30)

        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            database="НАЗВАНИЕ БД",
            user="ИМЯ ПОЛЬЗОВАТЕЛЯ",
            password="ПАРОЛЬ",
            port="5432"
        )
        cur = conn.cursor()

        # Получаем номер просроченного заказа за вчерашний день
        cur.execute("SELECT order_number FROM my_table WHERE date = %s", (yesterday,))
        expired_order = cur.fetchone()

        # Получаем список просроченных заказов за последние 30 дней
        cur.execute("SELECT order_number, date FROM my_table WHERE date >= %s AND date < %s", (thirty_days_ago, date.today()))
        expired_orders = cur.fetchall()

        # Закрываем соединение с базой данных
        cur.close()
        conn.close()

        # Отправляем сообщение пользователю, если есть просроченный заказ за вчерашний день
        if expired_order:
            message = f"Order {expired_order[0]} is overdue! Please contact the customer."
            bot.send_message(chat_id=chat_id, text=message)

        # Отправляем сообщение пользователю, если есть просроченные заказы за последние 30 дней
        if expired_orders:
            message = "The following orders have expired within the last 30 days:\n"
            for order in expired_orders:
                message += f"- {order[0]} (delivery date: {order[1].strftime('%Y-%m-%d')})\n"
            bot.send_message(chat_id=chat_id, text=message)
        else:
            bot.send_message(chat_id=chat_id, text="No expired orders found within the last 30 days.")

    # Запускаем функцию отправки сообщений о просроченных заказах в заданное время
    schedule.every().day.at(send_time).do(order)

    # Бесконечный цикл для проверки запланированных задач
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            break


# """
# добавляем обработчик команды /order и отправляет сообщение с заказом в указанное время.
order_handler = CommandHandler('order', order)
dispatcher.add_handler(order_handler)
send_order_message_at_time(bot, 'ID-ЧАТА', '12:38')



# Запускаем бота
updater.start_polling()
