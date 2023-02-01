from argparse import ArgumentParser, Namespace
import datetime
import requests
import json
import csv
import mysql.connector

url_weather = 'http://api.openweathermap.org/data/2.5/onecall'
api_weather = 'API WEATHER KEY'
api_city = 'NINJA API KEY'
url_city = 'https://api.api-ninjas.com/v1/geocoding'
days_available = [(datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0,7)]
today =datetime.datetime.now().strftime("%Y-%m-%d")
# print(type(days_available[0]))
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MYSQL password",
    database="weather_db",
)

mycursor=mydb.cursor()
mycursor2=mydb.cursor()

def get_lon_lat(city):

    response1 = requests.get(url_city, params={'city':args.city, 'country': args.country}, headers={'X-Api-Key': api_city})
    global lat
    lat = (response1.json()[0]['latitude'])
    global lon
    lon = (response1.json()[0]['longitude'])
    return lon, lat



def get_weather_data(city, date):
    # Use requests library to make a GET request to the weather API

    weather_params = {'lat': lat,
                      'lon': lon,
                      'city_name': city,
                      'appid': api_weather}
    # query_pre=("Select precipitation from forecast where city=%s and fcst_for_day=%s ")
    query_temp = ("Select temperature, precipitation from forecast where city=%s and fcst_for_day=%s and fcst_from=%s")
    params2 = (args.city,args.date, today)
    # mycursor.execute(query_pre, params2)
    mycursor.execute(query_temp, params2)

    myresult = mycursor.fetchall()

    row_count = mycursor.rowcount

    if row_count>0:
        for row in myresult:
            temperature = myresult[0][0]
            precipitation = myresult[0][1]
        print ('from my sql')

    else:
        try:
            response = requests.get(url_weather, weather_params)
            data = json.loads(response.text)
            print ('from API')
        # Parse the response to extract the temperature and precipitation data
            print (datetime.datetime.strptime(args.date, "%Y-%m-%d"))
            horizon = (datetime.datetime.strptime(args.date, "%Y-%m-%d")-datetime.datetime.today()).days+1
            temperature = int(data["daily"][horizon]["temp"]["max"])-273
            precipitation = data["daily"][horizon]["weather"][0]["main"]
        except IndexError:
            print('Enter valid city/country name')
        else:

            total_list=[]
            for i in range(0, 7):
                list_for_new = []
                list_for_new.append(today)
                list_for_new.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
                list_for_new.append(args.city)
                list_for_new.append(int(data["daily"][i]["temp"]["max"])-273)
                list_for_new.append(data["daily"][i]["weather"][0]["main"])
                total_list.append(list_for_new)
            # print(total_list)
            sql_del = 'delete from forecast where city=%s'
            params5=(args.city,)
            mycursor.execute(sql_del, params5)
            mydb.commit()
            if len(total_list)>0:
                for i in range (0, len(total_list)):
                    sql_ins = "Insert into forecast(fcst_from, fcst_for_day, city, temperature, precipitation) values (%s, %s, %s, %s, %s)"
                    params4 = total_list[i]
                    mycursor.execute(sql_ins, params4)
                    mydb.commit()

    return temperature, precipitation




if __name__ == "__main__":
    parser = ArgumentParser(description="Retrieve weather data for a given location and date")
    parser.add_argument("-c", "--city", default="Wrocław", help="The city for which to retrieve weather data")
    parser.add_argument("-l", "--country", default="", help="The country for which to retrieve weather data")
    parser.add_argument("-d", "--date", default=datetime.date.today(), choices=days_available ,help=f'The date for which to retrieve weather data (YYYY-MM-DD format) from {days_available}')
    parser.add_argument("-o", "--output", help="The file to which the weather data should be saved (in CSV format)")
    args : Namespace= parser.parse_args()

    try:
        lon, lat= get_lon_lat(args.city)
        temperature, precipitation = get_weather_data(args.city, args.date)


        if args.output:
            with open(args.output, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["Temperature", "Precipitation", "City", "Date"])
                writer.writerow([temperature, precipitation, args.city, args.date])
        else:
            print(f"Temperature: {temperature}")
            print(f"Precipitation: {precipitation}")
            print(f"City: {args.city}")
            print(f"Date: {args.date}")

    except IndexError:
        print('enter correct parameters')