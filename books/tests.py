from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book, Author, Genre
from books.api.serializers import BookSerializer
from datetime import date, timedelta

class BookSerializerAndViewTest(TestCase):

    def setUp(self):
        # Test client
        self.client = APIClient()

        # Authors
        self.author = Author.objects.create(
            name="John",
            bio="Columnist",
            date_of_birth=date(2002,12,26)
        )

        # Genres
        self.genre1 = Genre.objects.create(name="superhero")
        self.genre2 = Genre.objects.create(name="action")

        # Existing book
        self.book = Book.objects.create(
            title="Avengers",
            author=self.author,
            published_date=date.today() - timedelta(days=30)
        )
        self.book.genres.set([self.genre1, self.genre2])

    # -------------------------------
    # Serializer Tests
    # -------------------------------

    def test_serialization_output(self):
        """Test BookSerializer output contains correct fields"""
        serializer = BookSerializer(self.book)
        data = serializer.data
        self.assertEqual(data['title'], self.book.title)
        self.assertEqual(data['author_detail']['name'], self.author.name)
        self.assertIn(self.genre1.name, data['genres'])
        self.assertEqual(data['days_since_published'], 30)

    def test_deserialization_create(self):
        """Test creating a book from JSON data"""
        data = {
            "title": "Spider-Man",
            "author": self.author.id,
            "published_date": str(date.today() - timedelta(days=10)),
            "genres": [self.genre1.name, self.genre2.name]
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        book = serializer.save()
        self.assertEqual(book.title, "Spider-Man")
        self.assertEqual(book.genres.count(), 2)

    def test_title_validation(self):
        """Field-level validation: title length"""
        data = {
            "title": "A",
            "author": self.author.id,
            "published_date": str(date.today() - timedelta(days=1)),
            "genres": [self.genre1.name]
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_published_date_validation(self):
        """Object-level validation: published_date not in future"""
        future_date = date.today() + timedelta(days=5)
        data = {
            "title": "Future Book",
            "author": self.author.id,
            "published_date": str(future_date),
            "genres": [self.genre1.name]
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    # -------------------------------
    # View Tests (ListCreateAPIView)
    # -------------------------------

    def test_get_books_list(self):
        """GET /api/books/ returns list of books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book.title)

    def test_post_book_via_api(self):
        """POST /api/books/ creates a new book"""
        data = {
            "title": "Iron Man",
            "author": self.author.id,
            "published_date": str(date.today() - timedelta(days=5)),
            "genres": [self.genre1.name]
        }
        response = self.client.post('/api/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, "Iron Man")
