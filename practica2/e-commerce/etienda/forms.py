from django import forms

class productoForm(forms.Form):
	nombre = forms.CharField(label='Nombre', max_length=100)
	precio = forms.FloatField(label='Precio')
	categoria = forms.CharField(label='Categoria', max_length=100)
	descripcion = forms.CharField(label='Descripcion')
	imagen = forms.FileField(label='Imagen') # file porque image necesita plugin