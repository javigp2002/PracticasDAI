from django.shortcuts import render
from etienda.models import Consulta1, Consulta2, Consulta3, Consulta4, Consulta5, Consulta6
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    html = """
    <body>
        <h1>Práctica 2</h1>
        <ol>
            <li> <a href="C1/">C1</a> </li>
            <li> <a href="C2/">C2</a> </li>
            <li> <a href="C3/">C3</a> </li>
            <li> <a href="C4/">C4</a> </li>
            <li> <a href="C5/">C5</a> </li>
            <li> <a href="C6/">C6</a> </li>
        </ol>
    </body>

    """
    return HttpResponse(html)

def C1(request):
    salida = Consulta1()
    return HttpResponse(salida, content_type="text/plain")

def C2 (request):
    salida = Consulta2()
    return HttpResponse(salida, content_type="text/plain")

def C3 (request):
    salida = Consulta3()
    return HttpResponse(salida, content_type="text/plain")

def C4 (request):
    salida = Consulta4()
    return HttpResponse(salida, content_type="text/plain")

def C5 (request):
    salida = Consulta5()
    return HttpResponse(salida, content_type="text/plain")

def C6 (request):
    salida = Consulta6()
    return HttpResponse(salida, content_type="text/plain") 
