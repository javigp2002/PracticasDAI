from django import forms

def validate_nombre(value):
	if len(value) < 1:
		raise forms.ValidationError("El titulo debe contener un carácter mínimo")
	
	if value[0].islower():
		raise forms.ValidationError("El titulo debe empezar por mayúscula")


class productoForm(forms.Form):
	nombre = forms.CharField(label='Nombre', max_length=100)
	precio = forms.FloatField(label='Precio')
	categoria = forms.CharField(label='Categoria', max_length=100)
	descripcion = forms.CharField(label='Descripcion')
	imagen = forms.FileField(label='Imagen') # file porque image necesita plugin


