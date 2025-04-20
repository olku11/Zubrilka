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
otv_8_dv =[["Море Лаптевых", "1"], ["Восточно-Сибирское море", "2"], ["Чукотское море", "3"], ["Берингово море", "5"],
           ["Охотское море", "6"], ["Японское море", "7"], ["Пенжинская губа", "8"], ["залив Петра Велиого", "9"],
           ["Татарский пролив", "10"], ["пролив Лаперуза", "11"], ["Кунаширский пролив", "12"],
           ["п-ов. Камчатка", "13"], ["п-ов. Чукотка", "14"], ["о. Сахалин", "15"], ["Курильские о-ва", "16"],
           ["Восточно-Сибирское море", "17"], ["о. Врангеля", "18"], ["горы Джугджур", "19"],
           ["горы Сихотэ-Алинь", "20"], ["Чукотское нагорье", "21"], ["река Зея", "22"], ["оз. Ханко", "23"],
           ["р. Уссури", "24"], ["р. Камчатка", "25"], ["влк. Ключевская сопка", "26"],
           ["влк. Авачинская сопка", "27"], ["р. Анадырь", "28"], ["Зейское вдх.", "29"]]
otv_8_europe = [["Балтийское море", "1"], ["Финский залив", "1а"], ["Белое море", "2"], ["Баренцево море", "3"],
                ["Кандалакшкский залив", "4"], ["Онежская губа", "5"], ["Каспийское море", "6"],
                ["оз. Имандра", "7"], ["Беломоро-Балтийский канал", "8"], ["р. Онега", "9"], ["р. Мезень", "11"],
                ["р. Печора", "12"], ["р. Кама", "13"], ["р. Вятка", "14"], ["р. Нева", "15"],
                ["Мариинская система", "16"], ["Псковское оз.", "17"], ["оз. Ильмень", "18"], ["оз. Селигер", "19"],
                ["Рыбинское влх.", "20"], ["Горьковское вдх.", "21"], ["Куйбышевское вдх.", "22"],
                ["Волгоградское вдх.", "23"], ["Цимлянское вдх.", "24"], ["канал им. Москвы", "25"], ["р. Волга", "26"],
                ["р. Ока", "27"], ["р. Дон", "28"], ["Волго-Донской канал", "29"], ["г. Хибины", "30"],
                ["Тиманский кряж", "31"], ["Печорская низм.", "32"], ["Северные Увалы", "33"],
                ["Валдайская возв.", "34"], ["Мещерская низм.", "35"], ["Среднерусская возв.", "36"],
                ["Окско-Донская равн.", "37"], ["Приволжская возв.", "38"], ["Прикаспийская низм.", "39"],
                ["оз. Элтон", "40"], ["оз. Баскунчак", "41"], ["о. Ваалам", "42"], ["о. Кижи", "43"],
                ["п-ов. Рыбачий", "44"], ["Соловецкие о-ва.", "45"], ["п-ов. Канин", "46"], ["о-в. Колгуев", "47"],
                ["о-в. Вайгач", "48"]]
otv_8_ug = [["Чёрное море", "1"], ["Азовское море", "2"], ["Керченский пролив", "3"], ["Кавказские горы", "4"],
            ["р. Кубань", "5"], ["р. Кума", "6"], ["р. Терек", "7"], ["г. Эльбрус", "8"], ["г. Казбек", "9"],
            ["Таманский п-ов", "10"]]
otv_8_ural = [["хр. Пай-Хой", "1"], ["Полярный Урал", "2"], ["Приполярный Урал", "3"], ["Северный Урал", "4"],
              ["Средний Урал", "5"], ["Южный Урал", "6"], ["г. Народная", "7"], ["г. Качканар", "8"],
              ["г. Ямантау", "9"], ["г. Магнитная", "10"], ["р. Северная Сосьва", "11"], ["р. Кама", "12"],
              ["р. Чусовая", "13"], ["р. Тура", "14"], ["р. Исеть", "15"], ["р. Белая", "16"], ["р. Урал", "17"]]
otv_8_vossibir = [["п-ов. Таймыр", "1"], ["арх. Северная Земля", "2"], ["Новосибирские о-ва.", "3"],
                  ["г. Бырранга", "4"], ["плато Путорана", "5"], ["Среднесибирское плоскогорье", "6"],
                  ["Енисейский кряж", "7"], ["Верхоянский хребет", "8"], ["хребет Черского", "9"],
                  ["Яно-Оймяконское нагорье", "10"], ["Северо-Сибирская низм.", "11"],
                  ["Центрально-Якутская ранина", "12"], ["Яно-Индигирская низм.", "13"], ["Колымская низм.", "14"],
                  ["оз. Таймыр", "15"], ["р. Хатанга", "16"], ["р. Нижняя Тунгуска", "17"],
                  ["р. Подкаменная Тунгуска", "18"], ["р. Оленёк", "19"], ["р. Вилюй", "20"], ["Вилюйское вдх.", "21"],
                  ["р. Лена", "22"], ["р. Алдан", "23"], ["р. Яна", "24"], ["р. Индигирка", "25"], ["р. Колыма", "26"],
                  ["Карское море", "27"], ["море Лаптевых", "28"], ["Восточно-Сибирское море", "29"],
                  ["Енисейский залив", "30"], ["Западный Саян", "31"], ["Восточный Саян", "32"],
                  ["Ангарский кряж", "33"], ["Становое нагорье", "34"], ["Витиское плоскгорье", "35"],
                  ["Алданское нагорье", "36"], ["Становой хребет", "37"], ["р. Селенга", "38"], ["р. Шилка", "39"],
                  ["р. Аргунь", "40"]]
otv_8_zapsibir = [["Карское море", "1"], ["Байдарацкая губа", "2"], ["Обская губа", "3"], ["Енисейский залив", "4"],
                  ["п-ов. Ямал", "5"], ["Гыданский п-ов.", "6"], ["возв. Сибирские Увалы", "7"],
                  ["Ишимская равнина", "8"], ["Барабинская равнина", "9"], ["р. Пур", "11"], ["р. Таз", "12"],
                  ["р. Тобол", "13"], ["р. Ишим", "14"], ["оз. Чаны", "15"], ["Кулундинские озёра", "16"],
                  ["р. Катунь", "17"], ["р. Бия", "18"], ["Телецкое озеро", "19"], ["Салаирский кряж", "20"],
                  ["Кузнейский Алатау", "21"], ["г. Алтай", "22"], ["г. Белуха", "23"]]  ##22
otv_5_ostr = [[""]]
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
