from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)
    # books = models.ManyToManyField(Book, related_name='genres')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author,related_name='books', on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, related_name='books') 
    published_date = models.DateField()

    def __str__(self):
        return self.title




