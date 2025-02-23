from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to handle integrity errors that may occur when the ISBN is not unique.

        Returns:
            Response: A response object with the created book, or an error message if the ISBN is not unique.
        """
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({"error": "ISBN must be unique."}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def handle_exception(self, exc):
        """
        Handles exceptions raised by the view.

        If the exception is a `Book.DoesNotExist` exception, it will be
        caught and a 404 response will be returned with a JSON payload
        containing the error message.

        Otherwise, the exception will be passed to the parent class's
        `handle_exception` method for further handling.

        :param exc: The exception raised
        :return: A response object
        """
        if isinstance(exc, Book.DoesNotExist):
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
