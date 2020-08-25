from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="entryPage"),
    path("new_entry", views.newEntry, name="newEntry"),
    path("random_page", views.randomPage, name="randomPage"),
    path("edit_entry", views.editEntry, name="editEntry")
]
