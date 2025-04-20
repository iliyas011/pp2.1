import psycopg2
def get_paginated_records(limit, offset):
    try:
        with psycopg2.connect(host="localhost",
            database="phonebook",
            user="postgres",
            password="0000",
            port="5433") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_paginated_phonebook(%s, %s)", (limit, offset))
                for row in cur.fetchall():
                    print(row)
    except Exception as e:
        print("Ошибка:", e)

get_paginated_records(1, 1)
