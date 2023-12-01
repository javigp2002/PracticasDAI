from django.db import models
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
from django.contrib import messages
from django.shortcuts import render, redirect
from ninja import Schema



import requests
# Create your models here.
import logging
logger = logging.getLogger(__name__)

## CLASES
class Nota(Schema):
	rate: float = Field(ge=0., lt=5.)	
	count: int = Field(ge=1)
      
class Producto(Schema):
	title: str
	price: float
	description: str
	category: str
	image: str | None
	rating: Nota | None
      

	#comprobar que el title empieza por mayúscula
	# @field_validator('title')
	# @classmethod
	# def title_mayuscula(cls, v):
	# 	if v[0].islower():
	# 		raise ValueError('El título debe empezar por mayúscula')
	# 	return v.title()

class Compra(Schema):
	#_id: Any
	userId: int
	date: datetime
	products: list	



# Cliente
client = MongoClient('mongo', 27017)
tienda_db = client.tienda                   # Base de Datos
productos_collection = tienda_db.productos  # Coleccion  
compras_collection = tienda_db.compras  # Coleccion


###### funciones auxiliares
def get_quantities():
	ids_quantities = []
	compras_totales = compras_collection.find()

	for c in compras_totales:
		pc = c.get('products')
		for p in pc:
			ids_quantities.append([p.get('productId'), p.get('quantity')])
	
	return ids_quantities

def get_price_and_quantity(id):
    lista_productos_ids = []
    for prod in productos_collection.find():
        lista_productos_ids.append(prod.get('_id')) # autoinsertado por mongo

    prod = productos_collection.find_one({"_id":lista_productos_ids[id]})
    price_prod = prod.get('price')
    category = prod.get('category')
    
    return price_prod, category

def calcula_facturacion():
	facturacion_total = 0

	ids_quantities = get_quantities()
	
	for id in ids_quantities:
		id_on_list = id[0]-1 # los id de los productos empiezan en 1
		
		price_prod, category = get_price_and_quantity(id_on_list)

		facturacion_total += price_prod*id[1] # Cantidad comprada por precio
	return facturacion_total
		
def facturacion_por_categoria():
	facturacion_total_categoria = {}
	categories = productos_collection.distinct("category")
	for c in categories:
		facturacion_total_categoria[c] = 0

	ids_quantities = get_quantities()

	for id in ids_quantities:
		id_on_list = id[0]-1 # los id de los productos empiezan en 1
		price_prod, category = get_price_and_quantity(id_on_list)
		facturacion_total_categoria[category] += price_prod*id[1] # Cantidad comprada por precio de cada categoria

	return facturacion_total_categoria


def swap_id(productos):
	result = []
	for producto in productos:
		producto["id"] = str(producto.get('_id'))
		del producto["_id"]
		result.append(producto)

	return result


def busqueda_categoria(categoria):
	query = {}
	if categoria != "all":
		query = {"category": categoria}

	return swap_id(productos_collection.find(query,{"_id":1, "title": 1, "description": 1, "image": 1, "price":1}))


def busqueda_palabra(palabra):
	query = {"description": {"$regex" : palabra, "$options": "i"}}
	return swap_id(productos_collection.find(query,{"_id":1, "title": 1, "description": 1, "image": 1, "price":1}))

def add_producto(producto, request):
	try :
		productos_collection.insert_one(producto)

	except:
		logger.info("Error al añadir el producto")
		messages.success(request, "Producto añadido correctamente")

		return redirect('add')

	finally:
		logger.info("Producto añadido correctamente", producto['title'])
		if request != 0:
			messages.success(request, "Producto añadido correctamente")

######################### API ##############################

def consulta_productos():
	productos = productos_collection.find()
	resultado = []
	for producto in productos:
		producto["id"] = str(producto.get('_id'))
		del producto["_id"]
		resultado.append(producto)

	return resultado

# devuelve los productos desde el numero de item desde hasta el numero de item hasta
def get_productos(desde, hasta):
	productos = consulta_productos()[desde:hasta]

	return productos

def get_producto_by_id(id, solo_producto = True):
	producto = productos_collection.find_one({"_id": ObjectId(id)})
	producto["id"] = str(producto.get('_id'))
	del producto["_id"]
	if solo_producto:
		return producto
	else:
		return {"Producto": (producto)}

def add_producto_api(title, price, description, category, image):
	imagen = handle_uploaded_file(image)
	producto = recogerDatos(title, price, category, description, imagen)    
	objectid = productos_collection.insert_one(producto)
	logger.info("Producto añadido correctamente", producto['title'])
	
	return get_producto_by_id(objectid.inserted_id)

def handle_uploaded_file(f):
    path = 'static/imágenes/' + f.name
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f.name

# este también está en views.py
def recogerDatos(title, price, category, description, imagen):
    imagen = "imágenes/" + imagen
    producto = {
        "title": title,
        "price": price,
        "category": category,
        "description": description,
        "image": imagen,
    }

    return producto


def modify_product(producto, id):
	productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"title": producto.title, "price": producto.price, "description": producto.description, "category": producto.category}})
	logger.info("Producto " + id + " modificado correctamente")
	
	return get_producto_by_id(id)


def modify_rating(id, rating):
	product = productos_collection.find_one({"_id": ObjectId(id)}, {"rating": 1})
	logger.info("Producto " + id + " encontrado")

	if (product):
		new_rating = Nota(**product['rating'])

		new_count = new_rating.count +1
		new_rate = ((new_rating.rate * new_rating.count) + (rating * 1.0)) / new_count
		logger.info("New_count: " + str(new_rate))
	

		productos_collection.update_one({"_id": ObjectId(id)}, {"$set": {"rating": {"rate": new_rate, "count": new_count}}})
		logger.info("Producto " + id + " modificado correctamente")
		
		return get_producto_by_id(id)
	else:
		logger.error("Error al modificar el producto")
		return False
	
def delete_product(id):
	try:
		resul = productos_collection.find({"_id": ObjectId(id)})
		resultado = {}
		for attr, val in resul[0].items():
			if attr == "_id":
				resultado["id"] = str(val)
			else:
				resultado[attr] = val
		productos_collection.delete_one({"_id": ObjectId(id)})
		logger.info("Producto eliminado correctamente", resultado['title'])

		return resultado
	except Exception as e:
		logger.error(e)
		logger.error("Error al eliminar el producto")        
		return False
	