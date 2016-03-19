from django import template
from django.contrib.auth.models import User
from timetable.utils import pointsumm

register = template.Library()

def get_random_icon():
	import random
	icons = ('01', '02', '03', '05', '06', '07', '09', '10', '11', '12', '15', '16')
	return '/media/img/ny/xmas sticker-%s.png' % (random.choice(icons), )

@register.simple_tag(takes_context=True)
def get_vallet(context):
	request = context['request']
	return pointsumm(request.user)


register.simple_tag(get_random_icon)
#register.simple_tag(get_vallet)