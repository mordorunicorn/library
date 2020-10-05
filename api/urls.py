from django.urls import path

from api import views


urlpatterns = [
    path('authors', views.AuthorListView.as_view()),
    path('authors/<int:pk>', views.AuthorDetailView.as_view()),
    path('books', views.BookListView.as_view()),
    path('books/<int:pk>', views.BookDetailView.as_view()),
    path('series', views.SeriesListView.as_view()),
    path('series/<int:pk>', views.SeriesDetailView.as_view()),
]
