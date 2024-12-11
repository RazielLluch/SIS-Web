import mysql.connector
from config import SECRET_KEY, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, CLOUDINARY_CLOUD_NAME, \
    CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from config import LOCAL_SECRET_KEY, LOCAL_DB_PORT, LOCAL_DB_NAME, LOCAL_DB_USERNAME, LOCAL_DB_PASSWORD, LOCAL_DB_HOST
from mysql.connector import connect, Error


# set online to False if you want to connect to local database(laragon, localhost, etc.)
def connect_db(local=True):
    print('Connecting to MySQL database...')
    try:
        if local:
            db = connect(
                host=LOCAL_DB_HOST,
                user=LOCAL_DB_USERNAME,
                password=LOCAL_DB_PASSWORD,
                database=LOCAL_DB_NAME,
                port=int(LOCAL_DB_PORT),
            )
        else:
            db = connect(
                host=DB_HOST,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=int(DB_PORT),
            )
        cursor = db.cursor()
        return db, cursor
    except Error as e:
        print(f"Error connection: {e}")
