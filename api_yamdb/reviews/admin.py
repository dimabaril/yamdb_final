from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'title', 'score')
    list_editable = ('title',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Category)

admin.site.register(Genre)

admin.site.register(Title)

admin.site.register(GenreTitle)

# admin.site.register(Review)

admin.site.register(Comment)
