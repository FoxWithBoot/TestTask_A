from rest_framework import viewsets, generics, mixins, renderers
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
            return Response({'data': response.data}, template_name='home.html')
        return response

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return BookSerializer(self.queryset.values(*list(self.visibility)), **kwargs, fields=self.visibility)
        return BookSerializer(*args, **kwargs)


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

