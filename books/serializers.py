from rest_framework import serializers

from .models import Book, Profile


class DynamicFieldsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields) - {'id'}
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BookSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('column_name',)
