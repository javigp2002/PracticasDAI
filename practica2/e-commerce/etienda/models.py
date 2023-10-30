from django.db import models
from pymongo import MongoClient
from pydantic import BaseModel, FilePath, Field, EmailStr, field_validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
# Create your models here.

## CLASES
class Nota(BaseModel):
	rate: float = Field(ge=0., lt=5.)
	count: int = Field(ge=1)
      
class Producto(BaseModel):
	title: str
	price: float
	description: str
	category: str
	image: str | None
	rating: Nota | None
      

	#comprobar que el title empieza por mayúscula
	@field_validator('title')
	@classmethod
	def title_mayuscula(cls, v):
		if v[0].islower():
			raise ValueError('El título debe empezar por mayúscula')
		return v.title()

class Compra(BaseModel):
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



def busqueda_categoria(categoria):
	if categoria != "all":
		query = {"category": categoria}
		r = productos_collection.find(query,{"_id":0, "title": 1, "description": 1, "image": 1, "price":1})
	else:
		r = productos_collection.find({},{"_id":0, "title": 1, "description": 1, "image": 1, "price":1})
    
	return r


def busqueda_palabra(palabra):
    query = {"description": {"$regex" : palabra, "$options": "i"}}
    return  productos_collection.find(query,{"_id":0, "title": 1, "description": 1, "image": 1, "price":1})
        

def add_producto(producto):
    productos_collection.insert_one(producto)
    



###### CONSULTA ###
def Consulta1():
    r =  "\n\tElectronica entre 100 y 200E, ordenados por precio\n"
    query = {"category": "electronics", "price": {"$gt":100, "$lt":200}}
    for prod in productos_collection.find(query,{"_id":0, "title": 1, "price": 1}).sort("price", 1):
        r += "<p>"+ str(prod) + "</p>"
    
    return r

def Consulta2():
    r= "\n\tProductos que contengan la palabra 'pocket' en la descripcion\n"
    query = {"description": {"$regex" : "pocket", "$options": "i"}}
    for prod in productos_collection.find(query,{"_id":0, "title": 1, "description": 1}):
        r += "<p>"+ str(prod) + "</p>"

    return r

def Consulta3():
    r="\n\tProductos con puntuacion mayor de 4\n"
    query3= {"rating.rate": {"$gte":4}}
    for prod in productos_collection.find(query3,{"_id":0, "title": 1, "rating  ": 1}):
        r += str(prod) + "\n"    

    return r

def Consulta4():
    r="\n\tRopa de hombre, ordenada por puntuacion\n"
    query4={"category": "men's clothing"}
    for prod in productos_collection.find(query4,{"_id":0, "title": 1, "category":1, "rating":1}).sort("rating.rate", 1):
        r += str(prod) + "\n"
    return r

def Consulta5():
    r="\n\tFacturacion total\n"
    fact_str = str(calcula_facturacion())

    r+=("Facturacion total: " + fact_str + "\n")

    return r

def Consulta6():
    r =  "\n\tFacturacion por categoria de producto\n"
    r+="Facturacion por categoria:"
    r+= str(facturacion_por_categoria())
    return r
