from rest_framework import serializers
from .models import *
from .views import wiki2html
from user.serializers import *

class NoteSerializer(serializers.ModelSerializer):
	login = UserSerializer(many = False)	
	content = serializers.SerializerMethodField()

	def get_content(self, obj):
		return wiki2html(obj.content)

	class Meta:
		model = Note
		fields = (
			'id',	'title',	'content',	'views',	'login',
		)
		read_only_fields = ('id',)