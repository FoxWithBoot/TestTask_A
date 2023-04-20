from rest_framework import viewsets, generics, mixins, renderers
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
            #print(response.data[0].keys())
            return Response({'books': response.data, 'fields': self.visibility}, template_name='home.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(BookViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({"ddd":"ddd"})
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

