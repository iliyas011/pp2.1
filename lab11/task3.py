import psycopg2
def insert_many_users(surnames, names, numbers):
    try:
        with psycopg2.connect(host="localhost",
            database="phonebook",
            user="postgres",
            password="0000",
            port="5433") as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CALL insert_many_users(%s::text[], %s::text[], %s::text[])
                """, (surnames, names, numbers))
                conn.commit()
                print("Множественная вставка завершена.")
    except Exception as e:
        print("Ошибка:", e)

insert_many_users(
    ["Махабет", "Исаков", "Қосбармақ"],
    ["Асан", "Нурик", "Бекзат"],
    ["+77085471775", "+77770007777", "+77757760000"]
)
