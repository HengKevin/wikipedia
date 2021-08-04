from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name ="entry"),
    path("wiki/<str:entry>/edit", views.edit, name ="edit"),
    path("search", views.search, name="search"),
    path("newpage", views.newPage, name="newPage"),
    path("randompage", views.random, name="random")
]
