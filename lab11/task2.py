import psycopg2
def insert_or_update_user(surname, name, number):
    try:
        with psycopg2.connect(host="localhost",
            database="phonebook",
            user="postgres",
            password="0000",
            port="5433") as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_or_update_user(%s, %s, %s)", (surname, name, number))
                conn.commit()
                print("Добавлено или обновлено.")
    except Exception as e:
        print("Ошибка:", e)

insert_or_update_user("Кбту", "Асан", "+77085471775")
