from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Question

def changePollState(request, id, state):
	try:
		poll = Question.objects.get(id = id)
		if request.user.is_superuser or request.user == poll.login:
			if state == 'close': poll.is_closed = True
			else: poll.is_closed = False
			poll.save()
			return True
		else:
			raise ObjectDoesNotExist
	except ObjectDoesNotExist:		
		return False