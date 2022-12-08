"""Serializers."""
from rest_framework import exceptions, serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator


from api_yamdb.settings import (MESSAGE_FOR_RESERVED_NAME,
                                MESSAGE_FOR_USER_NOT_FOUND,
                                RESERVED_NAME)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом user.
    Зарезервированное имя использовать нельзя"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:

        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', )

    def validate_username(self, value):
        if value == RESERVED_NAME:

            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)

        return value


class ForAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей со статусом admin.
    Зарезервированное имя использовать нельзя"""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:

        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == RESERVED_NAME:

            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)

        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена.
    Зарезервированное имя использовать нельзя."""

    username = serializers.CharField(max_length=50, required=True)
    confirmation_code = serializers.CharField(max_length=50, required=True)

    def validate_username(self, value):

        if value == RESERVED_NAME:

            raise serializers.ValidationError(MESSAGE_FOR_RESERVED_NAME)

        if not User.objects.filter(username=value).exists():

            raise exceptions.NotFound(MESSAGE_FOR_USER_NOT_FOUND)

        return value


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:

        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:

        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """ Serializer for Title model."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:

        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category',)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Serializer for POST and PATCH methods for Title model."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:

        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:

        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
