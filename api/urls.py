from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('authors', views.AuthorViewSet)
router.register('books', views.BookViewSet)
router.register('series', views.SeriesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
