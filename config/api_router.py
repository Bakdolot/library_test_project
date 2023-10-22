from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("users/", include("library_test_project.users.urls")),
    path("books/", include("library_test_project.library.urls")),
]
