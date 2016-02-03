from rest_framework import serializers
from .models import *
from notes.serializers import NoteSerializer
from user.serializers import *

class FavoriteSerializer(serializers.ModelSerializer):
	login = UserSerializer(many = False)	
	note = serializers.SerializerMethodField()

	def get_note(self, obj):
		current_note = Note.objects.get(pk = obj.note.id)
		note = NoteSerializer(current_note, many = False, context = self.context)
		return note.data


	class Meta:
		model = Favorite
		fields = (
			'id',	'login',	'pub_date',	'note',	'file',
		)
		read_only_fields = ('id', 'login', 'note')