import requests
city = 'Moscow'
api = 'e804431e5f7d30136c5605c822b91c5e'


def daily(city):
    res = requests.get(f'http://api.openweathermap.org/data/2.5/weather',
                       params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': api})
    data = res.json()

    print("Город:", data['name'])
    print("Погодные условия:", data['weather'][0]['description'])
    print("Температура:", round(data['main']['temp']))
    print("Минимальная температура:", round(data['main']['temp_min']))
    print("Максимальная температура:", round(data['main']['temp_max']))
    print('Скорость ветра:', round(data['wind']['speed']))
    print('Видимость:', round(data['visibility']))


def week(city):

    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': api})
    data = res.json()
    print("Прогноз погоды на неделю:")
    for i in data['list']:
        print("Дата <", i['dt_txt'], "> \r\nТемпература <", '{0:+3.0f}'.format(i['main']['temp']),
              "> \r\nПогодные условия <", i['weather'][0]['description'], "> \r\nСкорость ветра <", round(i['wind']['speed']), "> \r\n Видимость <", i['visibility'], '>')
        print("____________________________")

daily(city)