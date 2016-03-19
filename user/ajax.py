from dajax.core import Dajax
from django.contrib.auth.models import User

def getrandomuser(request):
	import random
	dajax = Dajax()
	users = User.objects.all()
	result = random.choice(users)
	dajax.assign('#result', 'value', str(result.first_name + ' ' + result.last_name))
	return dajax.json()
