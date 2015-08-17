from django import forms

class EventAddForm(forms.Form):
	title = forms.CharField(label="Название", max_length=255)
	date = forms.DateTimeField(label="Дата и время события (в формате: 2015-01-25 14:15)")
	is_required = forms.BooleanField(label = 'Обязательно для посещения', required = False)
	description = forms.CharField(widget = forms.Textarea, label="Описание события", required = False)