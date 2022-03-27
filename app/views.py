from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection

from app.helper import queries

# Create your views here.
def index(request):
    """Shows the main page"""

    # ## Delete customer
    # if request.POST:
    #     if request.POST['action'] == 'delete':
    #         with connection.cursor() as cursor:
    #             cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['id']])


    # if request.POST:
    #     if request.POST['action'] == 'search':
    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #             "SELECT * FROM apartments WHERE country = %s AND city = %s AND num_guests >= %s",
    #             [
    #                 request.POST['country'],
    #                 request.POST['city'],
    #                 request.POST['num_guests']
    #             ])                
    #             apartments = cursor.fetchall()

    #             result_dict = {'records': apartments}

    #             return redirect(request,'search', result_dict)



    # ## Use raw query to get all objects
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM users ORDER BY first_name")
    #     users = cursor.fetchall()

    # result_dict = {'records': users}



    # return render(request,'app/index.html', result_dict)
    return render(request, 'app/index.html')



# Create your views here.
def view(request, userid):
    """
    Shows the view user details page, 
    which include user details and rental data
    """
    
    result_dict = dict()

    ## Use raw query to get a user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [userid])
        selected_user = cursor.fetchone()
    result_dict['user'] = selected_user

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * 
            FROM apartments ap, rentals r 
            WHERE ap.apartment_id = r.apartment_id 
            AND r.guest = %s""",
            [userid])
        selected_rentals = cursor.fetchall()

    result_dict['records'] = selected_rentals

    return render(request,'app/view.html', result_dict)



# Create your views here.
def add(request):
    """Shows the user registration page"""
    context = {}
    status = ''

    if request.POST:
        status = queries.insert_user(request.POST)

    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context = {}
    status = ''

    # # fetch the object related to passed email and password

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT * FROM users WHERE email = %s",
    #         [id]
    #         )
    #     obj = cursor.fetchone()

    # status = ''
    # # save the data from the form

    # if request.POST:
    #     ##TODO: date validation
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             "UPDATE users SET first_name = %s, last_name = %s, date_of_birth = %s, country = %s credit_card_type = %s credit_card_no = %s WHERE email = %s",
    #             [
    #                 request.POST['first_name'],
    #                 request.POST['last_name'],
    #                 request.POST['date_of_birth'],
    #                 request.POST['country'],
    #                 request.POST['credit_card_type'],
    #                 request.POST['credit_card_no'],
    #                 id
    #             ]
    #             )
    #         status = 'User edited successfully!'
    #         cursor.execute("SELECT * FROM users WHERE email = %s", [id])
    #         obj = cursor.fetchone()


    # context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)



def checkpw(request, userid):
    """Shows page to enter password and allow user to edit own details once password matches"""
    result_dict = {}
    status = ''

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            [userid]
            )
        obj = cursor.fetchone()

    if request.POST:
        if request.POST['action'] == 'enterpw':
        ## Check if email is already in the table
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", [id])
                user = cursor.fetchone()
                result_dict['user'] = user
            
                if user != None:
                    if user[3] == request.POST['password']:
                        return render(request, "app/edit.html", result_dict)
                    else:
                        status = 'Incorrect password'
                        context = {'status': status}
                        return render(request, "app/checkpw.html", context)

        elif request.POST['action'] == 'Update':
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET 
                    first_name = %s, 
                    last_name = %s, 
                    date_of_birth = %s, 
                    country = %s, 
                    credit_card_type = %s, 
                    credit_card_no = %s 
                    WHERE email = %s""",
                    [
                        request.POST['first_name'],
                        request.POST['last_name'],
                        request.POST['date_of_birth'],
                        request.POST['country'],
                        request.POST['credit_card_type'],
                        request.POST['credit_card_no'],
                        userid
                    ]
                    )
                status = 'User edited successfully!'
                cursor.execute("SELECT * FROM users WHERE email = %s", [userid])
                obj = cursor.fetchone()

            context = {'status': status}
            return render(request, "app/edit.html", context)

    context = {"status": status}
    return render(request, "app/checkpw.html")



def search(request):
    """Shows the search page for apartments"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                """
                SELECT * 
                FROM apartments apt, overall_ratings rts 
                WHERE apt.apartment_id = rts.apartment_id 
                AND country = %s 
                AND city = %s 
                AND num_guests >= %s 
                ORDER BY apt.price""",
                [
                    request.POST['country'],
                    request.POST['city'],
                    request.POST['num_guests']
                ])                
                apartments = cursor.fetchall()

            result_dict = {'records': apartments}

            return render(request,'app/search.html', result_dict)
    else:
        context['status'] = status
        ## Use sample query to get apartments

        """
        SQL VIEW ALREADY CREATED:

        CREATE VIEW overall_ratings AS
        SELECT ap.apartment_id, CAST(AVG(r.rating) AS DECIMAL(2, 1)) AS avg_rating
        FROM apartments ap, rentals r
        WHERE ap.apartment_id = r.apartment_id
        GROUP BY ap.apartment_id;
        """

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * 
                FROM apartments apt, overall_ratings rts 
                WHERE apt.apartment_id = rts.apartment_id 
                ORDER BY apt.price
                """),
            apartments = cursor.fetchall()

        result_dict = {'records': apartments}

        return render(request,'app/search.html', result_dict)


def apartment(request, apt_id):
    """Shows the apartment details page"""
    
    result_dict = dict()

    ## Use raw query to get an apartment
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * 
            FROM apartments apt, overall_ratings rts 
            WHERE apt.apartment_id = rts.apartment_id 
            AND apt.apartment_id = %s
            """,
            [apt_id])
        selected_apt = cursor.fetchone()
    result_dict['apt'] = selected_apt

    return render(request,'app/apartment.html', result_dict)



def users(request):
    """Shows all users in page"""
    
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['id']])



    ## Call function defined in db_fns.py
    ## which masks raw query in python function
    users = queries.get_all_users()

    result_dict = {'records': users}

    return render(request,'app/users.html', result_dict)