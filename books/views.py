# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Book
# from .serializers import BookSerializer
# from rest_framework import status

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