from ninja_extra import NinjaExtraAPI
from ninja import File, Form, Schema
from ninja.files import UploadedFile
from etienda.models import Producto, get_productos, get_producto_by_id, add_producto_api, modify_product

api = NinjaExtraAPI()
	
# function based definition
@api.get("/add", tags=['Aritmética'])
def add(request, a: int, b: int):
	return {"ok": "yes", "data": {"suma": a + b, "resta": a - b}}

@api.get("/productos", tags=['Productos'])
def get_prods_api(request, desde: int, hasta: int):
    return get_productos(desde, hasta)

@api.post("/productos", tags=['Productos'])
def add_prods_api(request, title: str = Form(...), price: float = Form(...), description: str = Form(...), category: str = Form(...), image: UploadedFile = File(...) ):
    return add_producto_api(title, price, description, category, image)

@api.get("/productos/<id>", tags=['Productos'])
def get_prod_by_id(request, id: str):
    return get_producto_by_id(id)
      
class ProductoSchema(Schema):
	title: str
	price: float
	description: str
	category: str
      
@api.put("/productos/<id>", tags=['Add'])
def update_product(request, id: str, producto: ProductoSchema):
    return modify_product(producto, id)
    


    