from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
	blog = BlogPost.objects.all().order_by('-id')
	feedback = Feedback.objects.all().order_by('-id')

	context = {
		'title': 'Новости + Предложения (Beta)',
		'blog': blog,
		'feedback': feedback
	}
	return render(request, 'feedback.html', context)