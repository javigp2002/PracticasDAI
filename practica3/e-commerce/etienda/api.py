from ninja_extra import NinjaExtraAPI
from ninja import File, Form, Schema
from ninja.files import UploadedFile
from etienda.models import Producto, get_productos, get_producto_by_id, add_producto_api, modify_product,delete_product, modify_rating
from ninja.security import HttpBearer

api = NinjaExtraAPI()

# class GlobalAuth(HttpBearer):
#     def authenticate(self, request, token):
#         if token == "DAI2023":
#             return token

# api = NinjaExtraAPI(auth=GlobalAuth())

class ProductoSchema(Schema):
	title: str
	price: float
	description: str
	category: str
    
class ErrorSchema(Schema):
	message: str
	

# function based definition
@api.get("/add", tags=['Aritmética'])
def add(request, a: int, b: int):
	return {"ok": "yes", "data": {"suma": a + b, "resta": a - b}}

@api.get("/productos", tags=['Productos'], response={200: list[ProductoSchema]})
def get_prods_api(request, desde: int, hasta: int):
    return 200, get_productos(desde, hasta)

@api.post("/productos", tags=['Productos'], response={200: ProductoSchema, 404: ErrorSchema})
def add_prods_api(request, title: str = Form(...), price: float = Form(...), description: str = Form(...), category: str = Form(...), image: UploadedFile = File(...) ):
    try:
        p = add_producto_api(title, price, description, category, image)
        return 200, p
    except Exception as e:
          return 404, {"message": "No se ha podido añadir el producto"}

@api.get("/productos/{id}", tags=['Productos'])
def get_prod_by_id(request, id: str):
    try:
        return 200,get_producto_by_id(id)
    except:
        return 404, {"message": "No se ha encontrado el producto"}
      
@api.put("/productos/{id}", tags=['Productos'])
def update_product(request, id: str, producto: Producto):
    try:
        return 200, modify_product(producto, id)
    except Exception as e:
        return 404, {"message": "No se ha encontrado el producto"}
    
    
@api.delete('/productos/<id>', tags=['Productos'], response={200: ProductoSchema, 404: ErrorSchema})
def delete_prod(request, id : str):
	try:
		resultado = delete_product(id)
		return resultado
	except Exception as e:
		return 404, {"message": "No se ha encontrado el producto"}
      


@api.put('/productos/{id}/{rate}', tags=['Productos'], response={200:Producto, 404: ErrorSchema})
def update_rating(request, id : str, rate: int):
    try:
        return modify_rating(id, rate)
    
    except Exception as e:
         return 404, {"message": "No se ha encontrado el producto"}

# @api.post("/token", auth=None) 
# def get_token(request, username: str = Form(...), password: str = Form(...)):
#     if username == "admin" and password == "DAI2324":
#         return {"token": "DAI2023"}
    