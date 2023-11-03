from django.shortcuts import render, redirect
from etienda.models import busqueda_categoria, busqueda_palabra, add_producto, Producto

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from etienda.forms import productoForm
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    logger.debug('index')
    logger.warning('He pasado por index')
    context = {
    }
    return render(request, 'etienda/index.html', context) #busca primero en templates por el settings.py

def busqueda(request):
    context = {
        'buscar' : request.GET.get('buscar'),
        'productos': busqueda_palabra(request.GET.get('buscar'))
    }
    return render(request, 'etienda/busqueda.html', context) #busca primero en templates por el settings.py


def bus_cat(request,busc):
    context = {
        'buscar' : request.GET.get('buscar'),
        'busc' : busc,
        'productos': busqueda_categoria(busc),
    }
    return render(request, 'etienda/bus_cat.html', context)

def add(request):
    form = productoForm()
    if request.method == 'POST':
        form = productoForm(request.POST, request.FILES)

        if form.is_valid():

            imagen = handle_uploaded_file(request.FILES['imagen'])
            producto = recogerDatos(form, imagen)
            add_producto(producto)

            messages.success(request, "Producto añadido correctamente")

            return redirect('index')
        else:
            logger.warning('Formulario no válido')
            messages.error(request, "Error en el formulario")
    context = {
        'form': form
    }
    return render(request, 'etienda/add.html', context)

def handle_uploaded_file(f):
    path = 'static/' + f.name
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f.name

def recogerDatos(form, imagen):
    producto = {
        "title": form.cleaned_data['nombre'],
        "price": form.cleaned_data['precio'],
        "category": form.cleaned_data['categoria'],
        "description": form.cleaned_data['descripcion'],
        "image": 'imágenes/' + imagen,
        "rating": {
            "rate": 4.8,
            "count": 17
        }
    }

    logger.warning(producto)
    return producto
