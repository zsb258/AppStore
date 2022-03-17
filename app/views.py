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

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY first_name")
        users = cursor.fetchall()

    result_dict = {'records': users}

    return render(request,'app/index.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the view details page"""
    
    ## Use raw query to get a user
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", [id])
        selected_user = cursor.fetchone()
    result_dict = {'user': selected_user}

    return render(request,'app/view.html', result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    insert_statement_sql = "INSERT INTO users (first_name, last_name, email, password, date_of_birth, country, credit_card_type, credit_card_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    if request.POST:
        ## Check if email is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users WHERE email = %s", [request.POST['email']])
            user = cursor.fetchone()
            ## No user with same email
            if user == None:
                ##TODO: date validation
                cursor.execute(
                    insert_statement_sql,
                    [
                    request.POST['first_name'],
                    request.POST['last_name'],
                    request.POST['email'],
                    request.POST['password'],
                    request.POST['date_of_birth'],
                    request.POST['country'],
                    request.POST['credit_card_type'],
                    request.POST['credit_card_no']
                    ])
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

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)