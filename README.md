# Book Manager API

This is a simple Django application for managing a list of books. It provides RESTful API endpoints to perform CRUD (Create, Read, Update, Delete) operations on books.

---

## Features

- **Book Model**:
  - Fields: `title`, `author`, `publication_date`, `isbn`, `summary`.
  - `publication_date` is validated to ensure it is in the past.
  - `isbn` is validated to ensure it is unique and either 10 or 13 digits long.

- **API Endpoints**:
  - `GET /api/books/`: Retrieve a list of all books.
  - `POST /api/book/`: Create a new book.
  - `GET /api/book/{id}/`: Retrieve a specific book by ID.
  - `PUT /api/book/{id}/`: Update a specific book by ID.
  - `DELETE /api/book/{id}/`: Delete a specific book by ID.

- **Validation**:
  - Ensures `isbn` is unique and valid.
  - Ensures `publication_date` is in the past.

- **Testing**:
  - Comprehensive unit tests cover all main functionalities, including edge cases and error handling.

---

## Code Structure

```
bookmanager/
├── books/
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Book model and validation logic
│   ├── serializers.py       # Serializers for the Book model
│   ├── tests.py             # Unit tests for the API
│   ├── urls.py              # URL routing for the API
│   └── views.py             # API views
├── bookmanager/
│   ├── __init__.py
│   ├── settings.py          # Django project settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── manage.py                # Django management script
└── README.md                # Project documentation
```

---

## Design Decisions

1. **Model Validation**:
   - Custom validators (`validate_isbn` and `validate_publication_date`) ensure data integrity at the model level.
   - The `isbn` field is unique to prevent duplicate entries.
   -  Add database indexing to `author` and `title` for faster retrieval

2. **API Design**:
   - RESTful API endpoints follow best practices for resource management.
   - Django REST Framework (DRF) is used for building the API, providing serialization, pagination, and error handling out of the box.

3. **Error Handling**:
   - Custom descriptive error messages are returned for invalid input (e.g., invalid ISBN, future publication date).
   - DRF's built-in exception handling is used for 404 (Not Found) and 400 (Bad Request) errors.

4. **Testing**:
   - Unit tests cover all CRUD operations, validation, and edge cases.
   - Test isolation is ensured by clearing the database before each test run.

5. **Pagination**:
   - Pagination is implemented to handle large datasets efficiently.
   - The default page size is set to 10, but this can be customized.

6. **Documentation**:
   - API documentation is generated using DRF Spectacular and Swagger UI, accessible at `/api/docs/`.

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Okemwag/bookmanager.git
   cd bookmanager
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the API**:
   - Visit `http://127.0.0.1:8000/api/books/` to interact with the API.
   - Visit `http://127.0.0.1:8000/swagger` for Swagger UI documentation.

---

## Running Tests

To run the unit tests:
```bash
python manage.py test
```

To check test coverage:
```bash
coverage run manage.py test
coverage report
```

---

## API Examples

### Create a New Book
**Request**:
```bash
POST /api/books/
{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "publication_date": "1925-04-10",
    "isbn": "9780743273565",
    "summary": "A story of the American Dream."
}
```

**Response**:
```json
{
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "publication_date": "1925-04-10",
    "isbn": "9780743273565",
    "summary": "A story of the American Dream."
}
```

### Retrieve All Books
**Request**:
```bash
GET /api/books/
```

**Response**:
```json
[
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publication_date": "1925-04-10",
        "isbn": "9780743273565",
        "summary": "A story of the American Dream."
    }
]
```

---

## Future Improvements

1. **Authentication**: Add user authentication to restrict access to certain endpoints.
2. **Search and Filtering**: Implement search and filtering for the book list.
3. **Deployment**: Containerize the application using Docker and deploy it to a cloud platform.
