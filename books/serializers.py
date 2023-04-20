from rest_framework import serializers

from .models import Book, Profile


class DynamicFieldsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        print(fields)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            print(allowed)
            existing = set(self.fields) - {'id'}
            print(existing - {'id'})
            print(existing - allowed)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
            #self.fields.
        #super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)
        # print(self.context)
        # fields = self.context.get('visibility')
        # if fields:
        #     allowed = set(fields)
        #     existing = set(self.fields.keys)
        #     for field_name in existing-allowed:
        #         self.fields.pop(field_name)


class BookSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
