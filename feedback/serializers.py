from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import *
from user.serializers import *
import markdown2

class BlogPostSerializer(serializers.ModelSerializer):
	login = UserSerializer(many = False)	
	content = serializers.SerializerMethodField()
	pub_date = serializers.SerializerMethodField()

	def get_content(self, obj):
		return markdown2.markdown(obj.content)

	def get_pub_date(self, obj):
		return obj.date.strftime("%Y-%m-%d %H:%M:%S")

	class Meta:
		model = BlogPost
		fields = (
			'id',	'title',	'login',	'content',	'pub_date'
		)
		read_only_fields = ('id',)