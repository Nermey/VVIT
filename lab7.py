import telebot
from telebot import types
from tokens import token
import psycopg2

bot = telebot.TeleBot(token)
conn = psycopg2.connect(database='timetable_mtuci',
                        user='postgres',
                        password='',
                        host='localhost',
                        port='5432')
cursor = conn.cursor()


def get_timetable(id1: int, id2: int):
    date: int
    week_num = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    if id1 == 0 or id1 == 30:
        date = 0
    elif id1 == 5 or id1 == 35:
        date = 1
    elif id1 == 10 or id1 == 40:
        date = 2
    elif id1 == 15 or id1 == 45:
        date = 3
    elif id1 == 20 or id1 == 50:
        date = 4
    elif id1 == 25 or id1 == 55:
        date = 5

    cursor.execute("SELECT s.name, tb.cab, time.name, teachers.name, s_type.name FROM timetable AS tb ""LEFT JOIN "
                   "subjects as s ON tb.sub_id = s.id JOIN time ON tb.time = time.id ""LEFT JOIN teachers ON "
                   "tb.teacher = teachers.id ""LEFT JOIN s_type ON tb.stype = s_type.id WHERE tb.id > %s AND tb.id < "
                   "%s ""ORDER BY tb.id", (id1, id2))
    records = list(cursor.fetchall())
    timetable = []
    for i in range(len(records)):
        subject = records[i]
        if subject[0] != 'Нет пары':
            timetable.append(f'{i + 1}.  Предмет: {subject[0]}\n'
                             f'Аудитория: {subject[1]}\n'
                             f'{subject[2]}\n '
                             f'Преподаватель: {subject[3]}\n'
                             f'{subject[4]}')
        else:
            timetable.append(f'{i + 1}.  {subject[0]}\n'
                             f'{subject[2]}')
    m_timetable = f'{week_num[date]}\n\n'
    for i in range(len(timetable)):
        m_timetable = m_timetable + timetable[i] + ('\n' * 2)
    return m_timetable


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('/help', '/mtuci',
                 '/monday', '/tuesday',
                 '/wednesday', '/thursday',
                 '/friday', '/saturday',
                 '/week', '/nextweek')
    bot.send_message(message.chat.id,
                     'Привет! Хочешь узнать свежую информацию о МТУСИ?',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, f'Описание:\n'\
                                        f'Команды:\n'\
                                        f'/start - запуск/перезапуск бота\n'\
                                        f'/help - показать справку\n'\
                                        f'/<день недели> - показать расписание на текущий день\n'\
                                        f'Пример: /monday\n'\
                                        f'/mtuci - показать информацию о МТУСИ\n'\
                                        f'/week - показать расписание на текущую неделю\n'\
                                        f'/nextweek - показать расписание на следующую неделю')


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'официальный сайт МТУСИ – https://mtuci.ru/')


@bot.message_handler(commands=['monday'])
def monday(message):
    timetable = get_timetable(0, 6)
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['tuesday'])
def tuesday(message):
    timetable = get_timetable(5, 11)
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['wednesday'])
def wednesday(message):
    timetable = get_timetable(10, 16)
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['thursday'])
def thursday(message):
    timetable = get_timetable(15, 21)
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['friday'])
def friday(message):
    timetable = get_timetable(20, 26)
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['saturday'])
def saturday(message):
    timetable = get_timetable(25, 31)
    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['week'])
def week(message):
    days_id = [(0, 6), (5, 11), (10, 16), (15, 21), (20, 26), (25, 31)]
    timetable = ''
    for i, j in days_id:
        timetable += get_timetable(i, j) + '\n'

    bot.send_message(message.chat.id, timetable)


@bot.message_handler(commands=['nextweek'])
def week(message):
    days_id = [(30, 36), (35, 41), (40, 46), (45, 51), (50, 56), (55, 61)]
    timetable = ''
    for i, j in days_id:
        timetable += get_timetable(i, j) + '\n'

    bot.send_message(message.chat.id, timetable)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() not in ['/help', '/mtuci', '/start', '/monday', '/tuesday']:
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю :(')


bot.polling(none_stop=True)
