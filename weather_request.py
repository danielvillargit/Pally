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
               return http_r.json()
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
    
    def sql_connect_forecast(self,dict_insert):
        
        #lst = [(a,b) for a,b in dict_insert.get('hourly').items() ]
        #lst = [ lst[i][1] for i in range(5)]
        
        
        
        df = pd.DataFrame.from_dict(dict_insert.get('hourly'))
        df.columns = ['time','temp','precipitation','cloudcover','visbility']
        print(df.head())
        import sqlite3
        con = sqlite3.connect("pally_meta.db")
        cur = con.cursor()
        
        
        
        
        
        cur.execute("CREATE TABLE IF NOT EXISTS forecast (time, temp, precipitation, cloudcover, visibility)")
        con.commit()
        
        df.to_sql('forecast',con,if_exists = 'replace')
        #cur.executemany("INSERT INTO forecast VALUES (?,?,?,?,?)", [(df[i] for i in range(5))] )
        
        cur.execute("SELECT * FROM forecast")
        for row in cur.fetchall():
            print(row)

    
if __name__ == "__main__":
    Htx = Weather(29.76,-95.36)
    x = Htx.forecastget()
    print(type(x))
    Htx.sql_connect_forecast(x)
    #y = Htx.airqualityget()
    #z = Htx.marineget(7)
    #a1 = Htx.marine_df_to_graph()
    

    #print(z)
    
    




