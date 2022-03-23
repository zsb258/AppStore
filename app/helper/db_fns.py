from django.db import connection


def dictfetchall_(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_all_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        records = dictfetchall_(cursor)
    return records

if __name__ == "__main___":
    records = get_all_users()
    for k, v in records:
        print(k, v)