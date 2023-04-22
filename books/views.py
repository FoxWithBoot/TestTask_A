from django.shortcuts import redirect
from rest_framework import viewsets, generics, mixins, renderers, status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import HTMLFormRenderer
from rest_framework.response import Response

from .models import Book, Profile
from .serializers import BookSerializer, ProfileSerializer


class BookViewSet(viewsets.ModelViewSet):
    visibility = Profile.objects.filter(is_visible=True).values_list('column_name', flat=True)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    renderer_classes = [renderers.BrowsableAPIRenderer, renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def list(self, request, *args, **kwargs):
        response = super(BookViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            all_fields = Profile.objects.all()
            return Response({'create_form': BookSerializer(),
                             'books': response.data,
                             'all_fields': ProfileSerializer(all_fields, many=True).data}, template_name='home.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(BookViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'serializer': self.get_serializer(response.data), 'book': response.data}, template_name='book_page.html')
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
            if serializer.is_valid():
                self.perform_create(serializer)
                return redirect('../books?format=html')

            vs_ls = list(self.visibility)
            vs_ls.append('id')
            books = BookSerializer(self.queryset.values(*vs_ls), fields=self.visibility, many=True)
            all_fields = ProfileSerializer(Profile.objects.all(), many=True)
            return Response({'create_form': serializer,
                             'books': books.data,
                             'all_fields': all_fields.data}, template_name='home.html')
        response = super().create(request, *args, **kwargs)
        return response

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            self.visibility = Profile.objects.filter(is_visible=True).values_list('column_name', flat=True)
            vs_ls = list(self.visibility)
            vs_ls.append('id')
            return BookSerializer(self.queryset.values(*vs_ls), **kwargs, fields=self.visibility)
        return BookSerializer(*args, **kwargs)


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

