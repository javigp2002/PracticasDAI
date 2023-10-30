from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("busqueda", views.busqueda, name="busqueda"),
    path("busq/<str:busc>", views.bus_cat, name="busc"),
    path("add", views.add, name="add"),

]