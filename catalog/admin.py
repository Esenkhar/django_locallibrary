from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

admin.site.register(Genre)


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]
    list_display = ('display_author_name', 'date_of_birth', 'date_of_death')
    inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    # fields = ['id', 'status', 'due_back']
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('author', 'genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # fields = ['book', 'imprint', 'borrower, 'status', 'due_back', 'id']
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'borrower', 'due_back')
        })
    )
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
