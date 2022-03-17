from readline import insert_text
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE email = %s", [request.POST['id']])


    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT * FROM apartments WHERE country = %s AND city = %s AND num_guests >= %s",
                [
                    request.POST['country'],
                    request.POST['city'],
                    request.POST['num_guests']
                ])                
                apartments = cursor.fetchall()

                result_dict = {'records': apartments}

                return redirect(request,'search', result_dict)



    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        users = cursor.fetchall()

    result_dict = {'records': users}

    return render(request,'app/index.html', result_dict)



# Create your views here.
def view(request, id):
    """Shows the view details page"""
    
    result_dict = dict()

    ## Use raw query to get a user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        selected_user = cursor.fetchone()
    result_dict['user'] = selected_user

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM apartments ap, rentals r WHERE ap.apartment_id = r.apartment_id AND r.guest = %s",
            [id])
        selected_rentals = cursor.fetchall()

    result_dict['records'] = selected_rentals

    return render(request,'app/view.html', result_dict)



# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if email is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users WHERE email = %s", [request.POST['email']])
            user = cursor.fetchone()
            ## No user with same email
            if user == None:
                ##TODO: date validation
                cursor.execute(
                    "INSERT INTO users (first_name, last_name, email, password, date_of_birth, country, credit_card_type, credit_card_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    [
                        request.POST['first_name'],
                        request.POST['last_name'],
                        request.POST['email'],
                        request.POST['password'],
                        request.POST['date_of_birth'],
                        request.POST['country'],
                        request.POST['credit_card_type'],
                        request.POST['credit_card_no']
                    ]
                    )
                return redirect('index')    
            else:
                status = 'User with email %s already exists' % (request.POST['email'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed email and password

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            [id]
            )
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET first_name = %s, last_name = %s, date_o_birth = %s, country = %s credit_card_type = %s credit_card_no = %s WHERE email = %s",
                [
                    request.POST['first_name'],
                    request.POST['last_name'],
                    request.POST['date_of_birth'],
                    request.POST['country'],
                    request.POST['credit_card_type'],
                    request.POST['credit_card_no'],
                    id
                ]
                )
            status = 'User edited successfully!'
            cursor.execute("SELECT * FROM users WHERE email = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)



def checkpw(request, id):
    result_dict = {}
    status = ''

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

        elif request.POST['action'] == 'Update':
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET first_name = %s, last_name = %s, date_o_birth = %s, country = %s credit_card_type = %s credit_card_no = %s WHERE email = %s",
                    [
                        request.POST['first_name'],
                        request.POST['last_name'],
                        request.POST['date_of_birth'],
                        request.POST['country'],
                        request.POST['credit_card_type'],
                        request.POST['credit_card_no'],
                        id
                    ]
                    )
                status = 'User edited successfully!'
                cursor.execute("SELECT * FROM users WHERE email = %s", [id])
                obj = cursor.fetchone()

            context = {'status': status}
            return render(request, "app/edit.html", context)

    context = {"status": status}
    return render(request, "app/checkpw.html")



def search(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        if request.POST['action'] == 'search':
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT * FROM apartments WHERE country = %s AND city = %s AND num_guests >= %s",
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
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM apartments ORDER BY price ASC")
            apartments = cursor.fetchall()

        result_dict = {'records': apartments}

        return render(request,'app/search.html', result_dict)