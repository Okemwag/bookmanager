from django.core.management import call_command
from django.db import transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book
from .serializers import BookSerializer


class BookTests(APITestCase):
    def setUp(self):
        with transaction.atomic():
            call_command('flush', verbosity=0, interactive=False)
            self.book = Book.objects.create(
                title="Test Book",
                author="Test Author",
                publication_date="2020-01-01",
                isbn="1234567890123",
                summary="Test Summary"
            )

    def test_get_all_books(self):     
        """
        Tests that a GET to the book list/create endpoint returns a paginated list of all books.
        """
        url = reverse('book-list-create')
        response = self.client.get(url)        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], self.book.title)

    def test_create_book(self):
        url = reverse('book-list-create')
        data = {
            "title": "New Book",
            "author": "New Author",
            "publication_date": "2021-01-01",
            "isbn": "9876543210987",
            "summary": "New Summary"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_invalid_isbn(self):
        url = reverse('book-list-create')
        data = {
            "title": "Invalid ISBN Book",
            "author": "Invalid Author",
            "publication_date": "2021-01-01",
            "isbn": "invalid-isbn",
            "summary": "Invalid ISBN Summary"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ISBN must contain only digits.", str(response.data))

    def test_create_book_duplicate_isbn(self):
        url = reverse('book-list-create')
        data = {
            "title": "Duplicate ISBN Book",
            "author": "Duplicate Author",
            "publication_date": "2021-01-01",
            "isbn": "1234567890123",  # Duplicate ISBN
            "summary": "Duplicate ISBN Summary"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book with this isbn already exists.", str(response.data))

    def test_get_single_book(self):
        url = reverse('book-retrieve-update-destroy', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_get_nonexistent_book(self):
        url = reverse('book-retrieve-update-destroy', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No Book matches the given query.", str(response.data))

    def test_update_book(self):
        url = reverse('book-retrieve-update-destroy', args=[self.book.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        url = reverse('book-retrieve-update-destroy', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_book_invalid_data(self):
        url = reverse('book-list-create')
        data = {
            "title": "",  
            "author": "",  
            "publication_date": "2100-01-01",  
            "isbn": "invalid-isbn", 
            "summary": ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field may not be blank.", str(response.data))  # Title and author are required
        self.assertIn("Publication date must be in the past.", str(response.data))
        self.assertIn("ISBN must contain only digits.", str(response.data))

    def tearDown(self):
        """
        Cleans up after each test case by flushing the database to ensure a clean state.
        """
        call_command('flush', verbosity=0, interactive=False)


class BookSerializerTests(APITestCase):
    def test_invalid_isbn(self):
        data = {
            "title": "Invalid ISBN Book",
            "author": "Invalid Author",
            "publication_date": "2021-01-01",
            "isbn": "invalid-isbn",
            "summary": "Invalid ISBN Summary"
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("ISBN must contain only digits.", str(serializer.errors))

    def test_future_publication_date(self):
        data = {
            "title": "Future Date Book",
            "author": "Future Author",
            "publication_date": "2100-01-01",
            "isbn": "1234567890123",
            "summary": "Future Date Summary"
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Publication date must be in the past.", str(serializer.errors))