from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .helpers import year
from users.models import User


MODELS_STR_MAX_LENGTH = 10


class Category(models.Model):
    """DB model for categories."""

    name = models.CharField(
        max_length=254,
        unique=True,
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
    )

    class Meta:

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:MODELS_STR_MAX_LENGTH]


class Genre(models.Model):
    """DB model for genres."""

    name = models.CharField(
        max_length=254,
        unique=True,
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
    )

    class Meta:

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:MODELS_STR_MAX_LENGTH]


class Title(models.Model):
    """DB model for titles."""

    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(
                year, 'Значение не должно быть больше текущей даты!'
            )
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=True,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:

        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:MODELS_STR_MAX_LENGTH]


class GenreTitle(models.Model):
    """DB model for many to many relation for Genre and Title models."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genretitles'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitles'
    )

    class Meta:

        verbose_name = 'ganretitle'
        verbose_name_plural = 'ganretitles'


class Review(models.Model):
    """DB model for reviews."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        'Rating',
        validators=[
            MinValueValidator(1, 'Minimum value - 1'),
            MaxValueValidator(10, 'maximum value - 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Creation date',
        auto_now_add=True,
    )

    class Meta:

        constraints = (models.UniqueConstraint(fields=('author', 'title'),
                                               name='unique_review'),)
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.text[:MODELS_STR_MAX_LENGTH]


class Comment(models.Model):
    """DB model for comments."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Creation date',
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text[:MODELS_STR_MAX_LENGTH]
