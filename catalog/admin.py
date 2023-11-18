from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse

from catalog.models import Book, BookInstance, Language

# Model Registration
# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Language)
# Admin Models

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ( 'title', 'author')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    search_fields = ( 'book__title', 'book__author', 'language__english_name', 'language__name')
    list_filter = ('status', 'due_back')
    list_display = ('display_title','display_author','display_language', 'due_back', 'status', 'borrower' )

    def display_title(self, obj):
        return obj.book.title if obj.book else ''

    def display_language(self, obj):
        if (obj.language): 
            return f'{obj.language.name} ({obj.language.english_name}) '
        else:
            return ''
    def borrower(self, obj):
        return obj.borrower.username if obj.borrower else ''


    def display_author(self, obj):
        return obj.book.author if obj.book else ''


    fieldsets = (
        (None, {
            'fields': ('book', 'id', 'language')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )




@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('english_name', 'name')