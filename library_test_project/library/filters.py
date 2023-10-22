from django_filters import rest_framework as filters

from .models import Book


class BookListFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="published_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="published_date", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["author", "genre"]
