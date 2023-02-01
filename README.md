# weather_api_database
Stores weather data from API in MySQL database. When next request comes, checks first if the data for location, day, and fcst from day is available is SQL database, if not it sends API requests , displays reuested value and stores all the data in the MySQL database (replacing prior values for a requested city).


The scripts needs to be run from terminal console, inside project location:

python main.py - to request values for default settings: city : Wroclaw and today's date

or adding any of the optional parameters according to below pattern:

python main.py -c Madrit -d 2023-02-03 -o "weather.csv" -l Spain

In case forecast for day, fcst from day (to present the latest value for the client) and for city exists in a database the value will be taken from SQL 
if not it will be taken from API
