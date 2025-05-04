import telebot
import time
from other import checkCity
from other import GetWeather
API_BOT = "" #@BotFather
bot = telebot.TeleBot(API_BOT)
user_cities = {}

def ButtonsBot():
    menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
    CheckWeather = telebot.types.KeyboardButton('🌤Узнать погоду')
    CheckOwner = telebot.types.KeyboardButton("😎Создатель")
    CheckTown = telebot.types.KeyboardButton("🌆Отправить местоположение", request_location=True)
    menu_keyboard.row(CheckWeather)
    menu_keyboard.row(CheckOwner,CheckTown)
    return menu_keyboard

@bot.message_handler(commands=["start"])
def StartBot(message):
    NameUser = message.from_user.first_name
    bot.reply_to(message, f"Привет, {NameUser}! Я бот, который подскажет какая погода у тебя в городе. Выбери нужную кнопку снизу и нажми её.", reply_markup=ButtonsBot())

@bot.message_handler(func=lambda message: message.text == "😎Создатель")
def OwnerBot(message):
    Text = '''
Приятно, что ты захотел узнать кто делал этого бота, создатель:
😎Имя - N/A
😍Юзернейм - N/A
🤖Другая информация - N/A
'''
    bot.reply_to(message, Text)

@bot.message_handler(content_types=['location'])
def CheckTown(message):
    lat = message.location.latitude
    lon = message.location.longitude
    user_cities[message.from_user.id] = checkCity.CheckCity(lat, lon) #Добавление города и айди в таблицу
    bot.reply_to(message, f"✅Город успешно определён! Ваш город: {user_cities[message.from_user.id]}🌤") 

@bot.message_handler(func=lambda message: message.text == "🌤Узнать погоду")
def CheckWeather(message):
    city = user_cities.get(message.from_user.id)
    if city is None:
        bot.reply_to(message, "❌Ваш город не определён! Сначало определите город кнопкой ниже.")
    else:
        weather_data = GetWeather.Weather(city)
        user_id = message.from_user.id
        
        weather_translation = {
    'clear': 'Ясно',
    'rain': 'Дождь',
    'clouds': 'Облачно',
    'snow': 'Снег',
    'thunderstorm': 'Гроза'
}
        Temp = weather_data['temp']
        weather = weather_data['weather']
        if Temp < 0:
            Cloth = "Термобельё"
        elif Temp < 10:
            Cloth = "Куртка"
        elif Temp < 20:
            Cloth = "Свитшот"
        else:
            Cloth = "Футболка"
        Acces = None
        if weather.lower() == "rain" or weather.lower() == "thunderstorm":
            Acces = "Дождевик или зонтик"

        temp_str = f"🌡 Температура: {weather_data['temp']}°C"
        feels_like_str = f"😊 Ощущается как: {weather_data['like']}°C"
        weather_str = f"☔ Погода: {weather_translation.get(weather_data['weather'].lower(), weather_data['weather'])}"
        wind = f"💨Скорость ветра: {weather_data['wind']} м/c"

        if Acces is None:
            help = f"👕По температуре {Temp}°C, вам лучше надеть {Cloth}"
        else:
            help = f"👕По температуре {Temp}°C, вам лучше надеть {Cloth} и также взять с собой {Acces}"
        
        message_text = f"""
----☀Текущая погода в {city}:----
{temp_str}
{feels_like_str}
{weather_str}
{wind}
----👔Помощь по выбору одежды:----
{help}
"""
        bot.send_message(user_id, message_text)

while True:
    time.sleep(5)
    try:
        bot.polling(none_stop=True, timeout=5)
    except Exception as e:
        print(e)
