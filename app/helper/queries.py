from django.db import connection
from django.db import IntegrityError

import re

from django.http import QueryDict


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


def check_user_exists(email: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            [email])
        
        user = cursor.fetchone()

        if user == None: return False
        else: return True



def insert_user(form: QueryDict) -> str:
    """
    Returns status message of the insertion
        If insertion is successful: return success message
        Else: return error message
    """
    status = ''

    user_exsts = check_user_exists(form['email'])
    if user_exsts:
        status = 'User with email %s already exists' % (form['email'])

    else:
        with connection.cursor() as cursor:
            ##TODO: date validation
            try:
                cursor.execute(
                    """
                    INSERT INTO users (
                        first_name,
                        last_name,
                        email,
                        password,
                        date_of_birth,
                        country,
                        credit_card_type,
                        credit_card_no
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    [
                        form['first_name'],
                        form['last_name'],
                        form['email'],
                        form['password'],
                        form['date_of_birth'],
                        form['country'],
                        form['credit_card_type'],
                        form['credit_card_no']
                    ]
                )
                status = 'Successfully inserted.'

            except IntegrityError as e:
                e_msg = str(e.__cause__)
                # regex search to find the column that violated integrity constraint
                constraint = re.findall(r'(?<=\")[A-Za-z\_]*(?=\")', e_msg)[1]
                status = f'Violated constraint: {constraint}. Please follow the required format.'
    
    return status



if __name__ == "__main___":
    records = get_all_users()
    for k, v in records:
        print(k, v)