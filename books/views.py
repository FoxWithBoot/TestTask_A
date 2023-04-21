from django.shortcuts import redirect
from rest_framework import viewsets, generics, mixins, renderers, status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import HTMLFormRenderer
from rest_framework.response import Response

from .models import Book, Profile
from .serializers import BookSerializer, ProfileSerializer


class BookViewSet(viewsets.ModelViewSet):
    visibility = None
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    renderer_classes = [renderers.BrowsableAPIRenderer, renderers.TemplateHTMLRenderer, renderers.JSONRenderer]
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        response = super(BookViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'books': response.data, 'fields': self.visibility}, template_name='home.html')
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
        else:
            response = super().update(request, *args, **kwargs)
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

