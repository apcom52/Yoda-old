from rest_framework import serializers
from .models import *
from user.serializers import *
from .views import get_file_ext_image

class LibraryTagCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = LibraryTagCategory
		fields = (
			'title',	'color',	'tags',
		)


class LibraryTagSerializer(serializers.ModelSerializer):
	color = serializers.SerializerMethodField()

	def get_color(self, obj):
		tag_category = LibraryTagCategory.objects.all().filter(librarytag__exact = obj)
		return tag_category[0].color

	class Meta:
		model = LibraryTag
		fields = (
			'id',	'title',	'views',	'color',
		)

class LibraryFileSerializer(serializers.ModelSerializer):
	size = serializers.SerializerMethodField()
	tags = LibraryTagSerializer(many = True)
	login = UserSerializer(many = False)
	icon = serializers.SerializerMethodField()
	#tags = serializers.StringRelatedField(many = True)

	def get_size(self, obj):
		return obj.file.size

	def get_icon(self, obj):
		return get_file_ext_image(obj.file.url)


	'''def get_tags_list(self, obj):
		return obj.tags'''

	class Meta:
		model = LibraryFile
		fields = (
			'id',	'title',	'description',	'file',	'tags',
			'pub_date',	'views',	'downloads',	'is_available',	
			'size',	'login',	'icon',
		)
		read_only_fields = ('id',)