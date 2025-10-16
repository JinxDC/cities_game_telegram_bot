from random import choice
import telebot
import geonamescache
import json
import wikipedia
import os.path as pt
import sqlite3

API_TOKEN = "TOKEN"
bot = telebot.TeleBot(API_TOKEN)

gc = geonamescache.GeonamesCache()
all_cities = gc.get_cities()
wikipedia.set_lang("ru")
cities = []
correct_format = [".png",".jpeg",".jpg"]
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(chat_id INT PRIMARY KEY, cities TEXT, score INT)")
con.commit()
con.close()
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("INSERT INTO users(chat_id, cities, score) VALUES(123,\"cities\", 234)")
con.commit()
con.close()

# def find_city(city):
#     city = city.upper()
#     for i in range(1, len(city) + 1):
#         letter = city[-i]
#         if letter in ['Ь', 'Ъ', 'Ы', 'Й']:  # неудачные буквы
#             continue
#         correct_names = []
#         for city_data in all_cities.values():
#             names = city_data.get("alternatenames", [])
#             for name in names:
#                 if name and name[0].upper() == letter and name not in cities:
#                     correct_names.append(name)
#         if correct_names:
#             return choice(correct_names)
#     return None

def find_city(letter):
    letter = letter.upper()
    for i in all_cities:
        names = all_cities[i].get("alternatenames")
        for name in names:
            if name:
                if name in cities:
                    break
                if name[0] == letter:
                    lat = all_cities[i].get("latitude")
                    lon = all_cities[i].get("longitude")
                    return name, lat, lon
    return None, 0, 0

def get_last_letter(city):
    if cities:
        last_city = cities[-1]
        last_letter = last_city[-1]
        if last_letter in ['Ь', 'Ъ', 'Ы', 'Й']:
            last_letter = last_city[-2]
        if city[0] == last_letter:
            return last_letter.upper()

# city = gc.search_cities(city)
# print(city)
# city_name = city[0].get("name")
# city_latitude = city[0].get("latitude")
# city_longitude = city[0].get("longitude")

def send_image(city_name, message):
    try:
        wikipedia.set_lang("ru")
        answer = wikipedia.search(city_name)
        if answer:
            page = wikipedia.page(answer[0])
            images = []
            print(0)
            for image in page.images:
                img_format = pt.splitext(image)[1]
                if img_format in correct_format:
                    images.append(image)
                print(img_format)
                print(1)
            if images:
                random_img = choice(images)
                bot.send_photo(message.chat.id, random_img)
            else:
                bot.send_message(message.chat.id, f"Картинка города {city_name} не найдена")
        else:
            bot.send_message(message.chat.id, f"Картинка города {city_name} не найдена")
    except Exception as exception:
        bot.send_message(message.chat.id, f"Произошла ошибка {exception}")
        print(f"Произошла ошибка: "
              f"\n\t{exception}")

def send_info(city_name, message):
    try:
        wikipedia.set_lang("ru")
        answer = wikipedia.search(city_name)
        if answer:
            text_info = wikipedia.summary(answer[0], sentences = 5)
            bot.send_message(message.chat.id, text_info)
        else:
            bot.send_message(message.chat.id, f"Информация о городе {city_name} не найдена")
    except Exception as exception:
        bot.send_message(message.chat.id, f"Произошла ошибка {exception}")
        print(f"Произошла ошибка: "
              f"\n\t{exception}")
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Здрасте")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    city = message.text.strip().title()
    if not gc.search_cities(city):
        bot.send_message(message.chat.id, "Такого города нет")
        return
    if city in cities:
        bot.send_message(message.chat.id, "Этот город уже был")
        return
    if city[0] == get_last_letter(city):
        bot.send_message(message.chat.id, "Буквы не совпадают")
        return
    # User
    city_info = gc.search_cities(city)
    city_latitude = city_info[0].get("latitude")
    city_longitude = city_info[0].get("longitude")
    bot.send_location(message.chat.id, city_latitude, city_longitude)
    send_info(city, message)
    send_image(city, message)
    cities.append(city)
    # Bot
    bot_city, lat, lon = find_city(city[-1])
    bot.send_message(message.chat.id, bot_city)
    bot.send_location(message.chat.id, lat, lon)
    send_info(bot_city, message)
    send_image(bot_city, message)
    cities.append(bot_city)

bot.infinity_polling()