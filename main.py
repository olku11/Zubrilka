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
otv_8_dv = [["Море Лаптевых", "1"], ["Восточно-Сибирское море", "2"], ["Чукотское море", "3"], ["Берингово море", "5"],
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
otv_5_ostr = [["п-ов. Лабрадор", "1"], ["п-ов. Калифорнийский", "2"], ["п-ов. Флорида", "3"], ["п-ов. Юкатан", "4"],
              ["Пиренейский п-ов.", "5"], ["Скандинавский п-ов.", "6"], ["Балканский п-ов.", "7"],
              ["п-ов Малая Азия", "8"], ["Аравиский п-ов.", "9"], ["п-ов. Африканский Рог", "10"],
              ["п-ов. Индостан", "11"], ["п-ов. Ямал", "12"], ["п-ов. Таймыр", "13"], ["Чукотский п-ов.", "14"],
              ["п-ов. Камчатка", "15"], ["п-ов. Корея", "16"], ["п-ов Индокитай", "17"], ["п-ов Малакка", "18"],
              ["п-ов. Кейп-Йорк", "19"], ["Большие Антильские о-ва.", "20"], ["о-в. Ньюфаундлен", "21"],
              ["о-в Виктория", "22"], ["Канадский Арктический Архипелаг", "23"], ["о-в. Баффинова Земля", "24"],
              ["о-в. Гренландия", "25"], ["о-в. Исландия", "26"], ["о-в. Ирландия", "27"], ["Британские о-ва", "28"],
              ["арх. Шпицберген", "29"], ["арх. Земля Франца Иосифа", "30"], ["арх. Новая Земля", "31"],
              ["арх. Северная Земля", "32"], ["Новосибирские о-ва", "33"], ["о-в. Мадагаскар", "34"],
              ["Курильские о-ва", "35"], ["Японские о-ва", "36"], ["Филиппинские о-ва", "37"], ["о-в. Суматра", "38"],
              ["о-в. Калимантан", "39"], ["о-в. Ява", "40"], ["о-в. Сулавеси", "41"], ["о-в. Новая Гвинея", "42"],
              ["Гавайские о-ва", "43"], ["о-в. Тасмания", "44"], ["о-ва Новая Зеландия", "45"],
              ["Антарктический п-ов.", "46"]]
otv_5_gori = [["Кордильеры", "1"], ["Аппалачи", "2"], ["Анды", "3"], ["Атлас", "4"], ["Кавказ", "5"], ["Урал", "6"],
              ["Гималаи", "7"], ["Драконовы горы", "8"], ["Большой Водораздельный хребет", "9"],
              ["влк. Котопахи", "10"], ["влк. Гекла", "11"], ["влк. Килиманджаро", "12"],
              ["влк. Ключевская Сопка", "13"], ["влк. Фудзияма", "14"], ["Тихий океан", "15"],
              ["Атлантический океан", "16"], ["Индийский океан", "17"], ["Южный океан", "18"],
              ["Северный Ледовитый океан", "19"], ["Скандинавские горы", "20"], ["Алтай", "21"],
              ["Горы Тянь-Шань", "22"], ["горы Памир", "23"], ["горы Гиндукуш", "24"], ["Тибет", "25"],
              ["горы Кунь-Лунь", "26"], ["влк. Орисаба", "27"], ["г. Арарат", "28"], ["влк. Кракатау", "29"]]
otv_5_prol = [["Залив Аляска", "1"], ["Калифорнийский залив", "2"], ["Мексиканский залив", "3"],
              ["Гудзонов залив", "4"],
              ["Ботнический залив", "5"], ["Обская губа", "6"], ["залив Шелихова", "7"], ["Анадырский залив", "8"],
              ["Бискайский залив", "9"], ["Гвинейский залив", "10"], ["Аденский залив", "11"],
              ["Персидски залив", "12"],
              ["Оманский залив", "13"], ["Бенгальский залив", "14"], ["Гудзовнов пролив", "15"],
              ["Датский пролив", "17"], ["Ла-Манш", "18"], ["Гибралтарский пролив", "19"], ["Пролив Дарданеллы", "20"],
              ["пролив Босфор", "21"], ["Суэцкий канал", "22"], ["Баб-эль-Мандебский пролив", "23"],
              ["Мозамбикский пролив", "24"], ["Малаккский пролив", "25"], ["Зондский пролив", "26"],
              ["Торресов пролив", "27"], ["Бассов пролив", "28"], ["Магелланов пролив", "29"], ["пролив Дрейка", "30"]]
otv_5_morya = [["море Бофорта", "1"], ["Карибское море", "2"], ["Саргассово море", "3"], ["Гренладское море", "5"],
               ["море Баффина ", "4"], ["Норвежское море ", "6"], ["Балтийское море", "7"], ["Баренцево море", "8"],
               ["Белое море ", "9"], ["Карское море", "10"], ["море Лаптевых", "11"], ["Восточно-Сибирское море", "12"],
               ["Чукотское море", "13"], ["Берингово море", "14"], ["Охотское море", "15"], ["Японское море", "16"],
               ["море Амундсена", "17"], ["море Уэдделла", "18"], ["море Росса", "19"], ["Тасманово море", "20"],
               ["Коралловое море", "21"], ["Средземное море", "22"], ["Чёрное море", "23"], ["Азовское море", "24"],
               ["Красное море", "25"], ["Аравийское море", "26"], ["Южно-Китайское море", "27"],
               ["Филиппинское море", "28"], ["Восточно-Китайское море", "29"]]
otv_5_reki = [["Река Юкон", "30"], ["река Маккензи", "31"], ["Большое Медвежье озеро", "32"],
              ["Большое Невольничье озеро", "33"], ["река Миссисипи", "34"], ["озеро Верхнее", "35"],
              ["озеро Мичиган", "36"], ["озеро Гурон", "37"], ["озеро Эри", "38"], ["озеро Онтарио", "39"],
              ["река Ориноко", "40"], ["река Амазонка", "41"], ["озеро Титикака", "42"], ["озеро Поопо", "43"],
              ["река Парана", "44"], ["река Парагвай", "45"], ["река Дунай", "46"], ["река Днепр", "47"],
              ["река Волга", "48"], ["Ладожское озеро", "49"], ["Онежское озеро", "50"], ["Каспийское море", "51"],
              ["река Тигр", "52"], ["река Евфрат", "53"], ["Аральское море", "54"], ["озеро Балхащ", "55"],
              ["река Амударья", "56"], ["река Сырдарья", "57"], ["река Обь", "58"], ["река Енисей", "59"],
              ["озеро Байкал", "60"], ["река Лена", "61"], ["река Амур", "62"], ["река Хуанхэ", "63"],
              ["река Янцзы", "64"], ["река Инд", "65"], ["река Ганг", "66"], ["река Брахмапутра", "67"],
              ["река Нигер", "68"], ["озеро Чад", "69"], ["озеро Виктория", "71"], ["озеро Танганьика", "72"],
              ["озеро Ньяса", "73"], ["река Нил", "70"], ["река Конго", "74"], ["река Замбези", "75"],
              ["река Лимпопо", "76"], ["озеро Эйр", "77"], ["река Дарлинг", "78"], ["река Муррей", "79"],
              ["озеро Восток", "80"]]
pols = dict()
ansver = []
k = 0
de = 0
msg = []


async def start(update, context):
    reply_keyboard = [['8 Класс', '5 класс']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(f"Привет! Добро пожаловать в Зубрилку!\n"
                                    f"Номенклатуру какого класса ты хочешь повторить?", reply_markup=markup)
    return 0


async def ans(update, context):
    if update.message.text.lower() == "8 класс":
        reply_keyboard = [['/8_gori', '/8_ostrova', '/8_morya'], ['/8_sosedi', '/8_reki', '/8_ravnini'],
                          ['/8_ug', '/8_eu', "/8_dv"], ["/8_ural", '/8_vsibir', "/8_zsibir"], ['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Тесты для 8 класса:\n"
                                        "/8_gori - Горы и хребты России \n"
                                        "/8_ostrova - Острова и полуострова России\n"
                                        "/8_morya - Моря, проливы и заливы России\n"
                                        "/8_reki - Реки и озёра России\n"
                                        "/8_sosedi - Соседи России\n"
                                        "/8_ravnini - Равнины, низменности и возвышенности России \n"
                                        "/8_ug - Юг России \n"
                                        "/8_eu - Европейская часть России \n"
                                        "/8_dv- Дальний Восток \n"
                                        "/8_ural - Урал \n"
                                        "/8_zsbir- Западная Сибирь \n"
                                        "/8_vsibir - Восточная Сибирь", reply_markup=markup)
        return ConversationHandler.END
    elif update.message.text.lower() == "5 класс":
        reply_keyboard = [['/5_ostr', '/5 gori', '/5_prol'], ['/5_morya', '/5_reki'], ['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Тесты для 5 класса:\n"
                                        "/5_gori - Горы и хребты мира \n"
                                        "/5_ostr - Острова и полуострова мира\n"
                                        "/5_prol - Проливы и заливы мира\n"
                                        "/5_reki - Реки и озёра мира\n"
                                        "/5_morya - Моря мира \n", reply_markup=markup)
        return ConversationHandler.END


async def stop_8(update, context):
    reply_keyboard = [['/8_gori', '/8_ostrova', '/8_morya'], ['/8_sosedi', '/8_reki', '/8_ravnini'],
                      ['/8_ug', '/8_eu', "/8_dv"], ["/8_ural", '/8_vsibir', "/8_zsibir"], ['/menu']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Тест прерван", reply_markup=markup)
    await update.message.reply_text("Тесты для 8 класса:\n"
                                    "/8_gori - Горы и хребты России \n"
                                    "/8_ostrova - Острова и полуострова России\n"
                                    "/8_morya - Моря, проливы и заливы России\n"
                                    "/8_reki - Реки и озёра России\n"
                                    "/8_sosedi - Соседи России\n"
                                    "/8_ravnini - Равнины, низменности и возвышенности России \n"
                                    "/8_ug - Юг России \n"
                                    "/8_eu - Европейская часть России \n"
                                    "/8_dv- Дальний Восток \n"
                                    "/8_ural - Урал \n"
                                    "/8_zsbir- Западная Сибирь \n"
                                    "/8_vsibir - Восточная Сибирь", reply_markup=markup)
    return ConversationHandler.END


async def gori_8_start(update, context):
    global otv_8_gori, pols
    prav = otv_8_gori
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_gori.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def ostr_8_start(update, context):
    global otv_8_ostr, pols
    prav = otv_8_ostr
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_ostr.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def prol_8_start(update, context):
    global otv_8_morya, pols
    prav = otv_8_morya
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_prol.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def reki_8_start(update, context):
    global otv_8_reki, pols
    prav = otv_8_reki
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_reki.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def sosedi_8_start(update, context):
    global otv_8_sosedi, pols
    prav = otv_8_sosedi
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_sosedi.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def vse8_centre(update, context):
    global pols
    al = pols[f'{update.message.chat.id}']
    prav = al[0]
    ansver = al[3]
    msg = al[2]
    k = al[1]
    k += 1
    ansver.append(update.message.text)
    while len(msg) > 0:
        await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg[-1].message_id)
        msg.pop()
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    if k == len(prav):
        return 1
    else:
        return 0


async def vse8_last(update, context):
    global pols
    al = pols[f'{update.message.chat.id}']
    prav = al[0]
    ansver = al[3]
    msg = al[2]
    k = al[1]
    ansver.append(update.message.text)
    while len(msg) > 0:
        await context.bot.delete_message(chat_id=update.message.chat.id, message_id=msg[-1].message_id)
        msg.pop()
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    st = ["НАЗВАНИЕ ВАШ_ОТВЕТ ПРАВИЛЬНЫЙ_ОТВЕТ ДА/НЕТ\n"]
    c = 0
    for i in range(len(prav)):
        if prav[i][1] == ansver[i]:
            st.append(f"{prav[i][0]}: {ansver[i]} {prav[i][1]} ДА \n")
            c += 1
        else:
            st.append(f"{prav[i][0]}: {ansver[i]} {prav[i][1]} НЕТ \n")
    print(st)
    await update.message.reply_text(" ".join(st), reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(
        f"Количесвто правильных ответов: {c}/{len(ansver)} {math.floor(c / len(ansver) * 100)}%",
        reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def vozv_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_vozv.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def ug_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_kavkaz.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def eu_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_europe.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def dv_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_dv.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def ural_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_ural.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def zsibir_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_zsib.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


async def vsibir_8_start(update, context):
    global otv_8_vozv, pols
    prav = otv_8_vozv
    random.shuffle(prav)
    ansver = []
    msg = []
    k = 0
    await context.bot.send_photo(chat_id=update.message.chat.id, photo=open("8_vsib.jpg", 'rb'))
    msg.append(await update.message.reply_text(f"Напишите цифру под которой обозначен данный объект: {prav[k][0]}",
                                               reply_markup=ReplyKeyboardRemove()))
    pols[f'{update.message.chat.id}'] = [prav, k, msg, ansver]
    return 0


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
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
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
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '/8_ug', '/8_eu', "/8_dv", "/8_ural", '/8_vsibir', "/8_zsibir", '/5_ostr', '/5 gori',
                            '/5_prol', '/5_morya', '/5_reki'], stop_8)]
    )
    conv_handler4 = ConversationHandler(
        entry_points=[CommandHandler('8_morya', prol_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler5 = ConversationHandler(
        entry_points=[CommandHandler('8_reki', reki_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler6 = ConversationHandler(
        entry_points=[CommandHandler('8_sosedi', sosedi_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler7 = ConversationHandler(
        entry_points=[CommandHandler('8_ravnini', vozv_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler8 = ConversationHandler(
        entry_points=[CommandHandler('8_ug', ug_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler9 = ConversationHandler(
        entry_points=[CommandHandler('8_eu', eu_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler10 = ConversationHandler(
        entry_points=[CommandHandler('8_dv', dv_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler11 = ConversationHandler(
        entry_points=[CommandHandler('8_ural', ural_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler12 = ConversationHandler(
        entry_points=[CommandHandler('8_vsibir', vsibir_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    conv_handler13 = ConversationHandler(
        entry_points=[CommandHandler('8_zsibir', zsibir_8_start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_centre)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, vse8_last)]

        },

        fallbacks=[
            CommandHandler(['stop', 'menu', '8_gori', '8_ostrova', '8_morya', '8_sosedi', '8_reki', '8_ravnini',
                            '8_ug', '8_eu', "8_dv", "8_ural", '8_vsibir', "8_zsibir", '5_ostr', '5 gori',
                            '5_prol', '5_morya', '5_reki', "pogoda"], stop_8)]
    )
    application.add_handler(conv_handler1)
    application.add_handler(conv_handler)
    application.add_handler(conv_handler2)
    application.add_handler(conv_handler3)
    application.add_handler(conv_handler4)
    application.add_handler(conv_handler5)
    application.add_handler(conv_handler6)
    application.add_handler(conv_handler7)
    application.add_handler(conv_handler8)
    application.add_handler(conv_handler9)
    application.add_handler(conv_handler10)
    application.add_handler(conv_handler11)
    application.add_handler(conv_handler12)
    application.add_handler(conv_handler13)
    application.run_polling()


main()
