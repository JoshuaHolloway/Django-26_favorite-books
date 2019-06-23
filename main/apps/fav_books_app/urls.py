from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^index$', views.index),

    # Register and Login
    url(r'^users/reg_login', views.reg_login),
    url(r'^users/reg',       views.register),
    url(r'^users/userLogin', views.userLogin),
    url(r'^users/logout',    views.logout),

    # Add
    url(r'^books/add', views.add),
    url(r'^books/show/(?P<book_id>\d+)$', views.show),

    # Edit

    # 5. Delete
    # URL                  Request   Server-Method   return
    # /users/<id>/delete   GET       delete()        redirect to /shows
    url(r'^books/(?P<book_id>\d+)/delete$', views.delete)  # /books/<id>/delete
]
