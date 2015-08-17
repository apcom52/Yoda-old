from django import forms

class AddPollForm(forms.Form):
	types = (
		(1, 'Один вариант ответа'),
		(2, 'Несколько вариантов ответа'),
	)

	title = forms.CharField(label = 'Заголовок опроса', min_length = 3, max_length = 128)
	type = forms.ChoiceField(label = 'Тип опроса', choices = types)
	is_anon = forms.BooleanField(label = 'Анонимный опрос', required = False)
	options = forms.CharField(label = 'Варианты ответа (перечисляйте через новую строку)', widget = forms.Textarea())

