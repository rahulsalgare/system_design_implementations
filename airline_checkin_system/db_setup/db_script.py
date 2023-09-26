import psycopg2
import names
from db_config import DB_PARAMS

try:
    connection = psycopg2.connect(**DB_PARAMS)

    cursor = connection.cursor()

    for i in range(120):
        name = names.get_full_name()
        cursor.execute(f"INSERT INTO users (name) VALUES ('{name}');")

    connection.commit()


except psycopg2.Error as e:
    print("Error connecting to the PostgreSQL database:", e)

finally:
    cursor.close()
    connection.close()
