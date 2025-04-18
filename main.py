import logging
import math
import json
import aiohttp
import requests
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler, _messagehandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
from glob import glob
from requests import post

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)
otv_8_gori = [['Гора Эльбрус', '1'], ['Гора Белуха', '2'], ['Вулкан Ключевская Сопка', '3'], ['Кавказские горы', '4'],
              ['Уральские горы', '5'],
              ['Горы Бырранга', '6'], ['Плато Путорана', '7'], ['Алтай', '8'], ['Западный Саян', '9'],
              ['Восточный Саян', '10'],
              ['Ангарский Кряж', '11'], ['Становое нагорье', '12'], ['Яблоновый хребет', '13'],
              ['Хребет Черского', '14'], ['Становой хребет', '15'],
              ['Сихотэ Алинь', '16'], ['Верхоянский хребет', '17'], ['Хребет Сунтар-Хаята', '18'],
              ['Хребет Джугджур', '19'], ['Колымское нагорье', '20'],
              ['Чукотское нагорье', '21'], ['Корякское нагорье', '22'], ['Срединный хребет', '23']]
otv_8_ostr = [["Крайняя западная точка: Балтийская коса", "1"], ["Крайняя материковая западная точка:  берег реки "
                                                                 "Педедзе", "2"], ["Мыс Челюскин", "3"],
              ["Крайняя южная точка: околы горы Рагдан", "4"], ["Мыс Дежнёва", "5"], ["арх. Новая Земля", "6"],
              ["арх. Земля Франца Иосифа", "7"], ["арх. Северная Земля", "9"], ["Новосибирские острова", "10"],
              ["остров Врангеля", "11"], ["ост. Ратманова", "12"], ["Курильские острова", "13"], ["ост. Сахалин", "15"],
              ["п-ов. Кольский", "16"], ["п-ов. Ямал", "17"], ["п-ов. Таймыр", "18"], ["Камчатка", "19"],
              ["Чукотский п-ов.", "20"], ["Крым", "21"]]  # 20
otv_8_morya = [["Чёрное море", "1"], ["Азовское море", "2"], ["Каспийское море", "3"], ["Балтийское море", "4"],
               ["Белое море", "5"], ["Баренцево море", "6"], ["Карское море", "7"], ["Море Лаптевых", "8"],
               ["Восточное-Сибирское море", "9"], ["Чукотское море", "10"], ["Берингово море", "11"],
               ["Охотское море", "12"], ["Японское море", "13"], ["Финский залив", "15"], ["Залив Шелихова", "17"],
               ["Обская губа", "16"], ["Анадырский залив", "18"], ["Татарский пролив", "19"], ["пролив Лаперуза", "20"],
               ["Кунаширский пролив", "21"], ["Берингов пролив", "23"], ["Пролив Лонга", "24"],
               ["пролив Вильицкого", "25"], ["пролив Карские ворота", "26"], ["Керченский пролив", "27"]]  # 25
otv_8_sosedi = [["Польша", "1"], ["Украина", "2"], ["Беларусь", "3"], ["Литва", "4"], ["Латвия", "5"], ["Эстония", "6"],
                ["Финляндия", "7"], ["Норвегия", "8"], ["Грузия", "9"], ["Абхазия", "10"], ["Южная Осетия", "12"],
                ["Азербайджан", "11"], ["Казахстан", "13"], ["Монголия", "14"], ["Китай", "15"], ["КНДР", "16"],
                ["Япония", "17"], ["США", "18"]]  # 18
otv_8_reki = [["Чудское озеро", "1"], ["Ладожское озеро", "2"], ["Онежское озеро", "3"], ["Байкал", "4"], ["Дон", "5"],
              ["Волга", "6"], ["Печора", "9"], ["Обь", "10"], ["Иртыш", "11"], ["Енисей", "12"], ["Ангара", "13"],  # 17
              ["Лена", "14"], ["Яна", "15"], ["Индигирка", "16"], ["Колыма", "17"], ["Анадырь", "18"], ["Амур", "19"]]
otv_8_vozv = [["Восточно-Европейская равнина", "1"], ["Западно-Сибирская равнина", "2"],
              ["Среднесибирское плоскогорье", "3"], ["Кумо-Манычская впадина", "4"], ["Прикаспийская низменность", "5"],
              ["Северо-Сибирская низменность", "6"], ["Валдайская возвышенность", "7"],
              ["Среднерусская возвышенность", "8"], ["Приволжская возвышенность", "9"], ["Северные Увалы", "10"]]  # 10

ansver = []
k = 0
de = 0
msg = 0


async def start(update, context):
    reply_keyboard = [['8 Класс', '7 класс', '5 класс']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"Привет! Добро пожаловать в Зубрилку!\n"
                                    f"Номенклатуру какого класса ты хочешь повторить?", reply_markup=markup)
    return 0


async def ans(update, context):
    if update.message.text.lower() == "8 класс":
        reply_keyboard = [['/8_gori', '/8_ostrova'], ['/8_morya ', '/8_reki'], ['/8_sosedi', '/8_ravnini'], ['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Тесты для 8 класса:\n"
                                        "/8_gori - Горы и хребты России \n"
                                        "/8_ostrova - Острова и полуострова \n"
                                        "/8_morya - Моря, проливы и заливы \n"
                                        "/8_reki - Реки и озёра \n"
                                        "/8_sosedi - Соседи \n"
                                        "/8_ravnini - Равнины, низменности и возвышенности", reply_markup=markup)
        return ConversationHandler.END
    elif update.message.text.lower() == "7 класс" or update.message.text.lower() == "5 класс":
        reply_keyboard = []
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Пока не сделано", reply_markup=markup)
        name = 0
        return ConversationHandler.END


async def stop_8(update, context):
    reply_keyboard = [['/8_gori', '/8_ostrova'], ['/8_morya ', '/8_reki'], ['/8_sosedi', '/8_ravnini'], ['/menu']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Тест прерван", reply_markup=markup)
    await update.message.reply_text("Тесты для 8 класса:\n"
                                    "/8_gori - Горы и хребты России \n"
                                    "/8_ostrova - Острова и полуострова \n"
                                    "/8_morya - Моря, проливы и заливы \n"
                                    "/8_reki - Реки и озёра \n"
                                    "/8_sosedi - Соседи \n"
                                    "/8_ravnini - Равнины, низменности и возвышенности", reply_markup=markup)
    return ConversationHandler.END


async def gori_8_start(update, context):
    global otv_8_gori, ansver, k, msg
    random.shuffle(otv_8_gori)
    ansver = []
    k = 0
    print(de)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_gori.jpg", 'rb'))
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_gori[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())

    return 0


async def gori_8_centre(update, context):
    global otv_8_gori, ansver, k, msg
    ansver.append(update.message.text)
    k += 1
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_gori[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())
    if k == 22:
        return 1
    else:
        return 0


async def gori_8_last(update, context):
    global otv_8_gori, ansver, msg
    ansver.append(update.message.text)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ \n"]
    c = 0
    for i in range(len(otv_8_gori)):
        if otv_8_gori[i][1] == ansver[i]:
            st.append(f"{otv_8_gori[i][0]}: {ansver[i]} {otv_8_gori[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{otv_8_gori[i][0]}: {ansver[i]} {otv_8_gori[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def ostr_8_start(update, context):
    global otv_8_ostr, ansver, k, msg
    random.shuffle(otv_8_ostr)
    ansver = []
    k = 0
    print(de)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_ostr.jpg", 'rb'))
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_ostr[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())

    return 0


async def ostr_8_centre(update, context):
    global otv_8_ostr, ansver, k, msg
    ansver.append(update.message.text)
    k += 1
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_ostr[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())
    if k == 19:
        return 1
    else:
        return 0


async def ostr_8_last(update, context):
    global otv_8_ostr, ansver, msg
    ansver.append(update.message.text)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ ДА/НЕТ\n"]
    c = 0
    for i in range(len(otv_8_ostr)):
        if otv_8_ostr[i][1] == ansver[i]:
            st.append(f"{otv_8_ostr[i][0]}: {ansver[i]} {otv_8_ostr[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{otv_8_ostr[i][0]}: {ansver[i]} {otv_8_ostr[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def prol_8_start(update, context):
    global otv_8_morya, ansver, k, msg
    random.shuffle(otv_8_morya)
    ansver = []
    k = 0
    print(de)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_prol.jpg", 'rb'))
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_morya[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())

    return 0


async def prol_8_centre(update, context):
    global otv_8_morya, ansver, k, msg
    ansver.append(update.message.text)
    k += 1
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_morya[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())
    if k == 24:
        return 1
    else:
        return 0


async def prol_8_last(update, context):
    global otv_8_morya, ansver, msg
    ansver.append(update.message.text)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ ДА/НЕТ\n"]
    c = 0
    for i in range(len(otv_8_morya)):
        if otv_8_morya[i][1] == ansver[i]:
            st.append(f"{otv_8_morya[i][0]}: {ansver[i]} {otv_8_morya[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{otv_8_morya[i][0]}: {ansver[i]} {otv_8_morya[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def reki_8_start(update, context):
    global otv_8_reki, ansver, k, msg
    random.shuffle(otv_8_reki)
    ansver = []
    k = 0
    print(de)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_reki.jpg", 'rb'))
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_reki[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())

    return 0


async def reki_8_centre(update, context):
    global otv_8_reki, ansver, k, msg
    ansver.append(update.message.text)
    k += 1
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_reki[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())
    if k == 16:
        return 1
    else:
        return 0


async def reki_8_last(update, context):
    global otv_8_reki, ansver, msg
    ansver.append(update.message.text)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ ДА/НЕТ\n"]
    c = 0
    for i in range(len(otv_8_reki)):
        if otv_8_reki[i][1] == ansver[i]:
            st.append(f"{otv_8_reki[i][0]}: {ansver[i]} {otv_8_reki[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{otv_8_reki[i][0]}: {ansver[i]} {otv_8_reki[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def sosedi_8_start(update, context):
    global otv_8_sosedi, ansver, k, msg
    random.shuffle(otv_8_sosedi)
    ansver = []
    k = 0
    print(de)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_sosedi.jpg", 'rb'))
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_sosedi[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())

    return 0


async def sosedi_8_centre(update, context):
    global otv_8_sosedi, ansver, k, msg
    ansver.append(update.message.text)
    k += 1
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_sosedi[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())
    if k == 17:
        return 1
    else:
        return 0


async def sosedi_8_last(update, context):
    global otv_8_sosedi, ansver, msg
    ansver.append(update.message.text)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ ДА/НЕТ\n"]
    c = 0
    for i in range(len(otv_8_sosedi)):
        if otv_8_sosedi[i][1] == ansver[i]:
            st.append(f"{otv_8_sosedi[i][0]}: {ansver[i]} {otv_8_sosedi[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{otv_8_reki[i][0]}: {ansver[i]} {otv_8_reki[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def vozv_8_start(update, context):
    global otv_8_vozv, ansver, k, msg
    random.shuffle(otv_8_vozv)
    ansver = []
    k = 0
    print(de)
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_vozv.jpg", 'rb'))
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_vozv[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())

    return 0


async def vozv_8_centre(update, context):
    global otv_8_vozv, ansver, k, msg
    ansver.append(update.message.text)
    k += 1
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg = await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {otv_8_vozv[k][0]}",
                                          reply_markup=ReplyKeyboardRemove())
    if k == 9:
        return 1
    else:
        return 0


async def vozv_8_last(update, context):
    global otv_8_vozv, ansver, msg
    ansver.append(update.message.text)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg.message_id)
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ ДА/НЕТ\n"]
    c = 0
    for i in range(len(otv_8_vozv)):
        if otv_8_vozv[i][1] == ansver[i]:
            st.append(f"{otv_8_vozv[i][0]}: {ansver[i]} {otv_8_vozv[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{otv_8_reki[i][0]}: {ansver[i]} {otv_8_reki[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    application = Application.builder().token('7662403975:AAH5Pu5PoIr9fX_H57leV1j1WUzu9zaEDqo').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, ans)]

        },

        fallbacks=[]
    )

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('8_gori', gori_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, gori_8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, gori_8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_reki', '8_sosedi', '8_ravnini'],
                           stop_8)]
    )
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('menu', start)],
        states={0: [MessageHandler(filters.TEXT & ~filters.COMMAND, ans)]
                },

        fallbacks=[]
    )
    conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler('8_ostrova', ostr_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, ostr_8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ostr_8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_reki', '8_sosedi', '8_ravnini'],
                           stop_8)]
    )
    conv_handler4 = ConversationHandler(
        entry_points=[CommandHandler('8_morya', prol_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, prol_8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, prol_8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_reki', '8_sosedi', '8_ravnini'],
                           stop_8)]
    )
    conv_handler5 = ConversationHandler(
        entry_points=[CommandHandler('8_reki', reki_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, reki_8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, reki_8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_reki', '8_sosedi', '8_ravnini'],
                           stop_8)]
    )
    conv_handler6 = ConversationHandler(
        entry_points=[CommandHandler('8_sosedi', sosedi_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, sosedi_8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, sosedi_8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_reki', '8_sosedi', '8_ravnini'],
                           stop_8)]
    )
    conv_handler6 = ConversationHandler(
        entry_points=[CommandHandler('8_ravnini', vozv_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vozv_8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vozv_8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_reki', '8_sosedi', '8_ravnini'],
                           stop_8)]
    )

    application.add_handler(conv_handler1)
    application.add_handler(conv_handler)
    application.add_handler(conv_handler2)
    application.add_handler(conv_handler3)
    application.add_handler(conv_handler4)
    application.add_handler(conv_handler5)
    application.add_handler(conv_handler6)
    application.run_polling()


main()
