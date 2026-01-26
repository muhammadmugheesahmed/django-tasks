from rest_framework.decorators import api_view
from rest_framework.response import Response
from books.models import Book,Author,Genre
from books.api.serializers import BookSerializer,AuthorSerializer,GenreSerializer,BookHyperlinkedSerializer
from rest_framework import status
from rest_framework import generics,viewsets


# ------------------cLASS BASED VIEW---------------


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookHyperlinkedViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookHyperlinkedSerializer

# ------------------FUNCTION BASED VIEW---------------

# @api_view(['GET', 'POST'])
# def book_list(request):

#     # GET → Read all books
#     if request.method == 'GET':
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)

#     # POST → Create a new book
#     elif request.method == 'POST':
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail(request, id):

#     try:
#         book = Book.objects.get(id=id)
#     except Book.DoesNotExist:
#         return Response(
#             {"error": "Book not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     # GET → Read single book
#     if request.method == 'GET':
#         serializer = BookSerializer(book)
#         return Response(serializer.data)

#     # PUT → Update book
#     elif request.method == 'PUT':
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE → Delete book
#     elif request.method == 'DELETE':
#         book.delete()
#         return Response(
#             {"message": "Book deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )