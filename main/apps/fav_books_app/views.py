from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Book
from datetime import datetime
import bcrypt
# ======================================================================================================================
def get_user_info(user_id):
    return {'user': User.objects.get(id=user_id)}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def get_all_users_info():
    return {'users': User.objects.all()}
# ----------------------------------------------------------------------------------------------------------------------
def get_book_info(book_id):
    return {'book': Book.objects.get(id=book_id)}
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def get_all_books_info():
    return {'books': Book.objects.all()}
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
def root(request):
    # Initialize session
    if 'user_logged_in' not in request.session:
        request.session['user_logged_in'] = {}
    return redirect("/users/reg_login")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def index(request):

    return render(request, "fav_books_app/index.html", get_all_books_info())
# ======================================================================================================================
def reg_login(request):
    return render(request, "fav_books_app/reg_login.html")
def validate(request):

    # Return true if no errors
    valid = False

    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST, User.objects.all())

    # check if the errors dictionary has anything in it
    if len(errors) > 0:

        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)

        # Errors found
        return valid

    else:
        # No erros => Valid
        valid = True
        return valid
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def register(request):

    valid = validate(request)
    if valid:

        # Grab values from form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password_orig = request.POST['password']

        # Hash Password
        password_hash = bcrypt.hashpw(password_orig.encode(), bcrypt.gensalt())

        # Create row in database
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash)

        messages.success(request, "Successfully registered")
        print("Successfully registered")
        return redirect("/users/reg_login")
    else: # not-valid
        # redirect the user back to the form to fix the errors
        return redirect("/users/reg_login")
# ======================================================================================================================
# ======================================================================================================================
def userLogin(request):

    # Grab email from form
    email = request.POST['email-login']

    # Grab row from database IF email is in database
    # TODO: Check to see if email is in database
    user = User.objects.get(email=email)

    # Grab entered password and test against stored hash
    password_login = request.POST['password-login']
    if bcrypt.checkpw(password_login.encode(), user.password_hash.encode()):
        print("password match")

        # Set Session with logged-in users info
        request.session['user_logged_in'] = {
            'id': user.id,
            'first_name': user.first_name,
            'logged_in': True
        }

        # Get one of the guys in this dictionary like so:
        #request.session['user_logged_in']['id']

        # return render(request, "wall_app/logged_in.html", {'user': user})
        return redirect("/index")
    else:
        print("failed password")
        return HttpResponse("You Loose!")
# ======================================================================================================================
def logout(request):
    request.session.pop('user_logged_in')
    return redirect("/")
# ======================================================================================================================
# ======================================================================================================================
# ======================================================================================================================
def add(request):
    title = request.POST['title']
    description = request.POST['description']
    user_id = request.session['user_logged_in']['id']
    user = User.objects.get(id=user_id)
    book = Book.objects.create(title=title, description=description, user=user)
    return redirect("/index")
# ======================================================================================================================
def show(request, book_id):
    context = get_book_info(book_id)
    book = Book.objects.get(id=book_id)

    # List of users who like the book
    users_who_like_book = Book.objects.first().users_who_like.all()

    context = {
        'book': Book.objects.get(id=book_id),
        'users_who_like_book': users_who_like_book
    }

    return render(request, "fav_books_app/show.html", context)
# ======================================================================================================================
def delete(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect("/index")
# ======================================================================================================================
def like(request, book_id):
    # Add this book to favorites list for specific-user

    user_id = request.session['user_logged_in']['id']
    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=book_id)


    #book.liked_books.add(user) # BACKWARDS - liked_books is effectively member of User class after reverse-lookup
    #user.liked_books.add(book)
    book.users_who_like.add(user)




    print(book.users_who_like.all())


    # To get a list of users who like a book:
    users_who_like_the_book = Book.objects.first().users_who_like.all()
    print(users_who_like_the_book)

    # To get the list of books a user likes:
    list_of_books_a_user_likes = User.objects.first().liked_books.all()
    print(list_of_books_a_user_likes)


    return redirect("/books/show/" + str(book_id))
