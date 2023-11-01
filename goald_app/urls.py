'''
File for defining url paths and corresponding handlers in Django notation
'''

from django.urls import path

from goald_app import views

urlpatterns = [
    path("", views.index, name="index"),

    path("login",    views.login,    name="login"),
    path("register", views.register, name="register"),

    path("create", views.create, name="create"),
    path("auth",   views.auth,   name="auth"),
    path("deauth", views.deauth, name="deauth"),
    path("change", views.change, name="change"),
    path("delete", views.delete, name="delete"),

    path("users",  views.users,  name="users"),
    path("duties", views.duties, name="duties"),
    path("goals",  views.goals,  name="goals"),

    path("home", views.home, name="home"),
]
