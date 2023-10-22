from django.urls import path

from .views import AddBookScoreView, AddCommentView, AddFavoriteView, BookDetailView, BookListView, DeleteFavoriteView

urlpatterns = [
    path("", BookListView.as_view()),
    path("<int:pk>", BookDetailView.as_view()),
    path("favorite", AddFavoriteView.as_view()),
    path("favorite/<int:pk>", DeleteFavoriteView.as_view()),
    path("comment", AddCommentView.as_view()),
    path("score", AddBookScoreView.as_view()),
]
