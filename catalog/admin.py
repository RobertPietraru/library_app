from django.contrib import admin

from catalog.models import Book, BookInstance, Language

admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Language)
# Register your models here.
