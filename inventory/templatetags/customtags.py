from django import template

register = template.Library()

def get_random_icon():
	import random
	icons = ('01', '02', '03', '05', '06', '07', '09', '10', '11', '12', '15', '16')
	return '/media/img/ny/xmas sticker-%s.png' % (random.choice(icons), )

register.simple_tag(get_random_icon)





'''def randomicon(value):
	import random
	icons = ('01', '02', '03', '05', '06', '07', '09', '10', '11', '12', '15', '16')
	return value.replace(arg, '/media/img/ny/xmas sticker-%s.png' % (random.choice(icons), ))'''