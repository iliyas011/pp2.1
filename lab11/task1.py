import psycopg2

def search_phonebook(pattern):
    try:
        with psycopg2.connect(host="localhost",
            database="phonebook",
            user="postgres",
            password="0000",
            port="5433") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
                for row in cur.fetchall():
                    print(f"{row[0]} {row[1]} — {row[2]}")
    except Exception as e:
        print("Ошибка:", e)

search_phonebook("М")
