from bs4 import BeautifulSoup
import requests


class Weather:
    @staticmethod
    def weather_check(city):
        city = city.split(" ")[1]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42 '
        }

        res = requests.get(
            f'https://www.google.com/search?q={city}погода&oq={city}погода&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7'
            f'&sourceid=chrome&ie=UTF-8',
            headers=headers
        )

        soup = BeautifulSoup(res.text, 'html.parser')

        time = soup.select('#wob_dts')[0].getText().strip()
        precipitation = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()

        return f'''День недели и время: {time}
Информация об осадках: {precipitation} 
Температура воздуха: {weather}°C'''
