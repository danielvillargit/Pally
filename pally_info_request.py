import requests

class Weather:
    
    def __init__(self):
        pass

    def forecastget(self):
        lat = 29.76
        long = -95.36
        string_api = r'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m,precipitation,cloudcover,visibility&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'.format(lat,long)
        r = requests.get(string_api)
        print(type(r.text))
        if r.status_code == 200:
               print("Successful Request Grab")
               return r
        else:
            raise Exception


if __name__ == "__main__":
    Wb = Weather()
    Wb.forecastget()



