import requests
from datetime import datetime,timedelta
import pandas as pd
import matplotlib.pyplot as plt

class Weather:
    
    def __init__(self,lat,long):
        pass
        self.lat = lat
        self.long = long


    def httprequest(self,http_string):

        http_r = requests.get(http_string)
        if http_r.status_code == 200:
               print("Successful Request Grab (200)")
               return http_r.text
        else:
            http_r.raise_for_status()
        
    def getdate(self):
        
        now = datetime.today()
        return now

    def forecastget(self):
        
        forecast_string = r'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m,precipitation,cloudcover,visibility&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'.format(self.lat,self.long)
        return self.httprequest(forecast_string)


    def airqualityget(self):

        air_string = r'https://air-quality-api.open-meteo.com/v1/air-quality?latitude={}&longitude={}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,dust,uv_index,us_aqi'.format(self.lat,self.long)
        return self.httprequest(air_string)

    def marineget(self,forecast_days):

        start_date = self.getdate()
        end_date = start_date + timedelta(forecast_days)
        
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        marine_string = r'https://marine-api.open-meteo.com/v1/marine?latitude={}&longitude={}&hourly=wave_height,wave_direction,wave_period,wind_wave_height,wind_wave_direction,wind_wave_period,wind_wave_peak_period&daily=wave_height_max,wave_direction_dominant,wave_period_max&timezone=America%2FChicago&start_date={}&end_date={}'.format(self.lat,self.long,start_date,end_date)
        return self.httprequest(marine_string)
    
    def marine_df_to_graph(self):
        
        df_json = pd.DataFrame.from_dict(eval(self.forecastget()))

        print(df_json)
        print(df_json.dtypes)
        print(df_json.info)
        
        df2 = pd.DataFrame(df_json['hourly']['temperature_2m'])

        df2.plot.line(subplots = True)
        plt.show()
        return df_json
    
if __name__ == "__main__":
    Htx = Weather(29.76,-95.36)
    x = Htx.forecastget()
    y = Htx.airqualityget()
    z = Htx.marineget(7)
    a1 = Htx.marine_df_to_graph()
    

    print(z)
    
    




