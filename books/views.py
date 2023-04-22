from django.shortcuts import redirect
from rest_framework import viewsets, mixins, renderers, status
from rest_framework.response import Response

from .models import Book, Profile
from .serializers import BookSerializer, ProfileSerializer


class BookViewSet(viewsets.ModelViewSet):
    visibility = None
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    renderer_classes = [renderers.BrowsableAPIRenderer, renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def list(self, request, *args, **kwargs):
        response = super(BookViewSet, self).list(request, *args, **kwargs)

        if request.accepted_renderer.format == 'html':
            all_fields = ProfileSerializer(Profile.objects.all(), many=True)
            print(type(all_fields.data))
            return Response({'create_form': BookSerializer(),
                             'books': response.data,
                             'all_fields': all_fields.data}, template_name='home.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(BookViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': BookSerializer(response.data), 'book': response.data}, template_name='book_page.html')
        return response

    def update(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response({'serializer': serializer, 'book': instance}, template_name='book_page.html', status=status.HTTP_200_OK)
            return Response({'serializer': serializer, 'book': instance}, template_name='err_ser.html', status=status.HTTP_400_BAD_REQUEST)
        response = super().update(request, *args, **kwargs)
        return response

    def create(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            serializer = self.get_serializer(data=request.data)
            response = super(BookViewSet, self).list(request, *args, **kwargs)
            all_fields = ProfileSerializer(Profile.objects.all(), many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return redirect('../books?format=html')
            return Response({'create_form': serializer,
                             'books': response.data,
                             'all_fields': all_fields.data}, template_name='home.html')
        response = super().create(request, *args, **kwargs)
        return response


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

