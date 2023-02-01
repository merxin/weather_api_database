# weather_api_database
Stores weather data from API in MySQL database. When next request comes, checks first if the data for location, day, and fcst from day is available is SQL database, if not it sends API requests , displays reuested value and stores all the data in the MySQL database (replacing prior values for a requested city).
