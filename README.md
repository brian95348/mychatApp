This project was designed using POSTGRESQL, to use sqlite3 as the database backend please just uncomment the sqlite3 settings in the settings.py file.

The channels require the docker server to be running in the background, run the following command:
docker run -p 6379:6379 -d redis:5
