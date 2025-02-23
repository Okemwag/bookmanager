from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date', 'isbn', 'summary']

    def validate_isbn(self, value):
        """
        Validator for ISBN. Checks that the ISBN is a 10 or 13 digit number.
        """
        if not value.isdigit():
            raise serializers.ValidationError("ISBN must contain only digits.")
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits long.")
        return value

    def validate_publication_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Publication date must be in the past.")
        return value