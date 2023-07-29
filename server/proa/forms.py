# En forms.py
from django import forms

class ImportarAlumnosForm(forms.Form):
    archivo_excel = forms.FileField(label='Seleccione el archivo Excel', widget=forms.FileInput(attrs={'accept': '.xlsx'}))
