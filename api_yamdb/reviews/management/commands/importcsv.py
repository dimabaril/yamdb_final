"""Filler."""
from csv import DictReader
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    GenreTitle
)
from users.models import User


class Command(BaseCommand):
    """Importing csv file in local db."""

    help = (
        'Import list of files from static/data/:'
        + 'category.csv, comment.csv, genre.csv, genre_title.csv, review.csv,'
        + ' title.csv and user.csv'
    )

    def handle(self, *args, **option):
        """Filler."""
        print("Loading DB data")

        for row in DictReader(open('./static/data/users.csv')):
            user = User.objects.get_or_create(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            print(user)

        print('Users done..')

        for row in DictReader(open('./static/data/category.csv')):
            category = Category.objects.get_or_create(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            print(category)

        print('Categories done..')

        for row in DictReader(open('./static/data/genre.csv')):
            genre = Genre.objects.get_or_create(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            print(genre)

        print('Genres done..')

        for row in DictReader(open(
            './static/data/titles.csv',
            encoding='utf-8'
        )):
            title = Title.objects.get_or_create(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category'])
            )
#            title = Title.objects.get(pk=row['id'])
#            for rows in DictReader(open('./static/data/genre_title.csv')):
#                if rows['title_id'] == row['id']:
#                    title.genre.get_or_create(
#                        name=Genre.objects.get(pk=rows['genre_id'])
#                    )

            print(title)

        print('Tiltes done..')

        for row in DictReader(open('./static/data/genre_title.csv')):
            genre_title = GenreTitle.objects.get_or_create(
                pk=row['id'],
                genre=Genre.objects.get(pk=row['genre_id']),
                title=Title.objects.get(pk=row['title_id'])
            )
            print(genre_title)

        print('Genres of titles done..')

        for row in DictReader(open(
            './static/data/review.csv',
            encoding='utf-8'
        )):
            review = Review.objects.get_or_create(
                pk=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            print(review)

        print('Reviews done..')

        for row in DictReader(open(
            './static/data/comments.csv',
            encoding='utf-8'
        )):
            comment = Comment.objects.get_or_create(
                author=User.objects.get(pk=row['author']),
                review=Review.objects.get(pk=row['review_id']),
                text=row['text'],
                pub_date=row['pub_date']
            )
            print(comment)

        print('Comments done..')
        print('DB filled')
