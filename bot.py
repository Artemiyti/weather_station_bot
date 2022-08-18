import requests
import datetime
from config import BOT_TKN, WTR_TKN
from weather_handler import data_handler, wind_direction, time_control, location_list
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=BOT_TKN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello! choose one of the locations WFR, WWA, Depot or Dixie")


@dp.message_handler(commands=["info"])
async def info_command(message: types.Message):

    for i in location_list:
        data = data_handler(i)
        try:
            await message.reply(f"***{data['T']}***\n"
                                f"Location: {i}\nTemperature: {data['TA']}C°\n"
                                f"Humidity: {data['RH']}%\nPressure: {data['BA'][1]} millibars\nWind: {data['WI'][1]} m/s\n"
                                f"Wind direction: {data['WI'][2]}° {wind_direction(int(data['WI'][2]))}\n"
                                f"Peak wind: {data['GU'][1]}m/s {data['GU'][2]}° {wind_direction(int(data['WI'][2]))}\n"
                                f"Visibility: {data['VI']} miles\n"
                                f"Cloud height: {data['CL'][2]}m {data['CL'][3]}m {data['CL'][4]}m {data['CL'][5]}m\n"
                                f"Cloud height status: {data['CL'][1]}\n"
                                f"Lightning distance: {data['LD'][1]} {data['LD'][1]} {data['LD'][1]} {data['LD'][1]}\n"
                                f"***Have a nice day!***")
        except Exception as ex:
            await message.reply(f" Location: {i}\n data is corrupted or missing\n {ex}")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Drizzle \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }

    if message.text in location_list:
        try:
            data = data_handler(message.text)
            if time_control(data['T']) is True:
                await message.reply(f"***{data['T'].replace(',', '  ')}***\n"
                      f"Weather in {message.text}\nTemperature: {data['TA']}C°\n"  
                      f"Humidity: {data['RH']}%\nPressure: {data['BA'][1]} millibars\nWind: {data['WI'][1]} m/s\n"
                      f"Wind direction: {data['WI'][2]}° {wind_direction(int(data['WI'][2]))}\n"
                      f"Peak wind: {data['GU'][1]}m/s {data['GU'][2]}° {wind_direction(int(data['WI'][2]))}\n"
                      f"Visibility: {data['VI']} miles\n"
                      f"Cloud height: {data['CL'][2]}m {data['CL'][3]}m {data['CL'][4]}m {data['CL'][5]}m\n"
                      f"Cloud height status: {data['CL'][1]}\n"
                      f"Lightning distance: {data['LD'][1]} {data['LD'][1]} {data['LD'][1]} {data['LD'][1]}\n"
                      f"***Have a nice day!***")
            else:
                await message.reply(f"\U00002620 Data is outdated \U00002620 \n"
                                    f"The last data was received more than three hours ago\n"  
                                    f"Notify the operator immediately!")
        except Exception as ex:
            print(ex)
            await message.reply(f"\U00002620 Something wrong!\U00002620 \n"
                                f"Notify the operator immediately!")

    else:

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WTR_TKN}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Look out the window, I don’t understand what the weather is like there!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                  f"Weather in {city}\nTemperature: {cur_weather}C° {wd}\n"
                  f"Humidity: {humidity}%\nPressure: {pressure} mmHg\nWind: {wind} m/s\n"
                  f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLength of the day: {length_of_the_day}\n"
                  f"***Have a nice day!***")
        except:
            await message.reply("\U00002620 Check city name \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)

