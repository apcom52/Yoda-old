from django import forms
from .models import Note

class NoteAddForm(forms.Form):
	title = forms.CharField(label="Название", max_length=255)
	content = forms.CharField(widget = forms.Textarea, label="Содержимое")

class NoteEditForm(forms.Form):
	title = forms.CharField(label="Название", max_length=255)
	content = forms.CharField(widget = forms.Textarea, label="Содержимое")