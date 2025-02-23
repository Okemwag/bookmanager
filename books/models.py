from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_isbn(value):
    """
    Validator for ISBN. Checks that the ISBN is a 10 or 13 digit number.
    """
    
    if not value.isdigit():
        raise ValidationError("ISBN must contain only digits.")
    if len(value) not in [10, 13]:
        raise ValidationError("ISBN must be 10 or 13 digits long.")

def validate_publication_date(value):
    """
    Validator for publication date. Ensures that the publication date is not set in the future.
    Raises a ValidationError if the date is in the future.
    """

    if value > timezone.now().date():
        raise ValidationError("Publication date must be in the past.")

class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=100, db_index=True)
    publication_date = models.DateField(validators=[validate_publication_date])
    isbn = models.CharField(max_length=13, unique=True, validators=[validate_isbn])
    summary = models.TextField(blank=True, null=True)

    def __str__(self)-> str:
        return self.title
    
    class Meta:
        ordering = ['title']