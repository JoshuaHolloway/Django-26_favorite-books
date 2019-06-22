from django.shortcuts import render, redirect
def index(request):
    return render(request, "fav_books_app/index.html")
