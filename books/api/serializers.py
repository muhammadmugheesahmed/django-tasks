from rest_framework import serializers
from books.models import Book,Author,Genre
from datetime import date


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name', 'bio', 'date_of_birth']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name']
        


class BookSerializer(serializers.ModelSerializer):
    # Nested author info for read-only
    author_detail = AuthorSerializer(source='author', read_only=True)
    # Author ID for writing
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),write_only=True)
    # genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    genres = serializers.SlugRelatedField( many=True, queryset=Genre.objects.all(), slug_field='name' )

    # Custom computed field
    days_since_published = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title','author', 'author_detail', 'published_date', 'days_since_published', 'genres']
        depth = 1  # Includes nested author info automatically

    # SerializerMethodField to calculate days since published
    def get_days_since_published(self, obj):
        return (date.today() - obj.published_date).days

    # Field-level validation
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters long.")
        return value

    # Object-level validation
    def validate(self, data):
        published_date = data.get('published_date')
        if published_date and published_date > date.today():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return data


    # # Handle ManyToMany field properly
    # def create(self, validated_data):
    #     genres_data = validated_data.pop('genres', [])
    #     book = Book.objects.create(**validated_data)
    #     book.genres.set(genres_data)  # assign multiple genres
    #     return book

    # def update(self, instance, validated_data):
    #     genres_data = validated_data.pop('genres', None)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     if genres_data is not None:
    #         instance.genres.set(genres_data)
    #     return instance

#  ---------------Hyperlinked serializer for navigable APIs------------

class BookHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    genres = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'author', 'genres', 'published_date']
        extra_kwargs = {
            'url': {'view_name': 'book-detail', 'lookup_field': 'pk'}
        }


#  -----------Custom relational field for Author -> Books-------------

class AuthorBooksField(serializers.RelatedField):
    """Custom relational field that shows book title and year"""
    def to_representation(self, value):
        return f"{value.title} ({value.published_date.year})"