import psycopg2 as ps

def get_connection():
    conn = ps.connect(
        dbname="movies",
        user="your_username",
        password="your_password",
        host="localhost",
        port="5432"
    )
    return conn