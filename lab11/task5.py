import psycopg2
def delete_data(name, phone):
    try:
        with psycopg2.connect(host="localhost",
            database="phonebook",
            user="postgres",
            password="0000",
            port="5433") as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_data(%s, %s)", (name, phone))
                conn.commit()
                print("Удалено.")
    except Exception as e:
        print("Ошибка:", e)

delete_data(None, "+77085471775")  # Удалит по номеру
