from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import *
from .views import wiki2html
from user.serializers import *
from favorites.models import Favorite

class NoteSerializer(serializers.ModelSerializer):
	login = UserSerializer(many = False)	
	content = serializers.SerializerMethodField()
	in_favorite = serializers.SerializerMethodField('get_gin_favorite')
	pub_date = serializers.SerializerMethodField()

	def get_content(self, obj):
		return wiki2html(obj.content)

	def get_pub_date(self, obj):
		return obj.pub_date.strftime("%Y-%m-%d %H:%M:%S")

	def get_gin_favorite(self, obj):
		profile = self.context['request'].user
		try:
			fav = Favorite.objects.all().filter(login = profile, type = 1, note = obj)
			if fav:
				return True
		except ObjectDoesNotExist:
			return False
		return False

	class Meta:
		model = Note
		fields = (
			'id',	'title',	'content',	'views',	'login',	'in_favorite',
			'pub_date',
		)
		read_only_fields = ('id',)