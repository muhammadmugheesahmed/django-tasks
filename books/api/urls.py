from django.urls import path,include
# from books.api.views import book_list,book_detail 
from rest_framework.routers import DefaultRouter
from books.api.views import (BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView,
                            AuthorListCreateAPIView,AuthorRetrieveUpdateDestroyAPIView,
                            GenreListCreateAPIView,GenreRetrieveUpdateDestroyAPIView,BookHyperlinkedViewSet )

# Router for hyperlinked API
router = DefaultRouter()
router.register(r'books-detail', BookHyperlinkedViewSet, basename='book-detail')

urlpatterns = [
    # path('books/', book_list),
    # path('books/<int:id>/', book_detail),  
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    
    path('authors/', AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorRetrieveUpdateDestroyAPIView.as_view(), name='authors-detail'),

    path('genre/', GenreListCreateAPIView.as_view(), name='genre-list-create'),
    path('genre/<int:pk>/', GenreRetrieveUpdateDestroyAPIView.as_view(), name='genre-detail'),

       # Hyperlinked API
    path('', include(router.urls)),

]
