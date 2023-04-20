from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('client/', client_render)
]

print(router.urls)