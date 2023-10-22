from django.contrib import admin

from .models import Author, Book, Comment, Genre, UserFavoriteBooks

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(UserFavoriteBooks)
