from django.db import models
import re # regex module

# Custom manager for validation
class UsersManager(models.Manager):
    def basic_validator(self, postData, users):

        # Validation 1: Does name contain numbers?
        def hasNumbers(inputString):  # https://stackoverflow.com/a/19859308
            return any(char.isdigit() for char in inputString)

        errors = {}
        # add keys and values to errors dictionary for each invalid field

        # Validation 1 and 2:
        # Ensures names are at least of minimum length and do not contain numbers
        min_name_len = 1
        if len(postData['first_name']) < min_name_len or hasNumbers(postData['first_name']):
            errors["first_name"] = "first-name should be at least " + str(min_name_len) + " characters"
        if len(postData['last_name']) < min_name_len or hasNumbers(postData['last_name']):
            errors["last_name"] = "last-name should be at least " + str(min_name_len) + " characters"

        #  Validation 3: Does email have proper form?
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # create a regular expression object
        if not EMAIL_REGEX.match(postData['email']):  # test whether a field matches the pattern
            errors["email"] = "email does not have proper form"

        # Validation 4: Does second password match first?
        if(postData['password'] != postData['password-confirm']):
            errors["password"] = "Password entered does not match confirmation"

        # Validation 5: Ensure email is not already in database
        for user in users:
            if user.email == postData["email"]:
                errors["email_in_db"] = "Already registered!"
            break

       # TODO: Change to do the email validation in one of the following ways:
       #  1. User.objects.get(email=email)
       #    -If there is not a matching email for a .get(), Django throws an error (try and except could come in handy),
       #     otherwise it returns the User object associated with the matching user.e.g.Userobject.
       #  2. User.objects.filter(email = email)
       #     -Filter, on the other hand, returns a list, so if there is no user that matches,
       #      it returns an empty list.If there is a single matching user the list will contain a single User object:
       #      e.g.[Userobject].

        return errors
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# TODO: Below I copied in the Books/Authors (w. templates) models.py file
#       Only changed Author to User
#       and related_name="authors"
#       to  related_name="users"
#       AND also copied in the Users model from Django-25_the-wall
#  -The difference in this project is:
#   1. Author is called User
#   2. Author(Users) still has many-to-many relationship,
#      but now Authors(Users) has a one to many relationship with book also.
#   3. The many-tom-many relationship now has the intermediate table of
#      "favorites" instead of "books_authors"
# ======================================================================================================================
class User(models.Model): # Cntrl+Alt+F7

    # From The-Wall
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

    ## From Books w. Templates
    #books = models.ManyToManyField(Book, related_name="users")

    def __repr__(self):
        return f"User: ({self.first_name}, {self.last_name}, {self.email}, {self.password_hash})"
# ======================================================================================================================
# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=255)
  description    = models.TextField()
  uploaded_by    = models.ForeignKey(     User, related_name="books") # books_uploaded
  users_who_like = models.ManyToManyField(User, related_name="liked_books") # books_uploaded

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __repr__(self):
    return f"Book: ({self.title})"
