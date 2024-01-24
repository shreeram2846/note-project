from rest_framework import serializers
from .models import Note


class NoteShareSerializer(serializers.ModelSerializer):
    # Serializer for updating the shared_with field of a Note
    class Meta:
        model = Note
        # Specify the fields to include in the serializer
        fields = ['shared_with']


class NoteSerializer(serializers.ModelSerializer):
    # Serializer for the Note model
    class Meta:
        model = Note
        # Specify the fields to include in the serializer
        fields = ['id', 'title', 'content', 'owner', 'created_at', 'updated_at']
        # Specify read-only fields that should not be modified by the serializer during updates
        read_only_fields = ['owner', 'created_at', 'updated_at']

