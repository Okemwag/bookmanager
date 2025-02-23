from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    """
    list_display = ('title', 'author', 'publication_date', 'isbn')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('publication_date',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'publication_date', 'isbn', 'summary')
        }),
    )
    
