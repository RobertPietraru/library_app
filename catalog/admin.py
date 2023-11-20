from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse

from catalog.models import Book, BookInstance, Language
admin.site.unregister(User)

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



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'custom_row')
    def custom_row(self, obj):
        # Replace this with the actual data you want to display in the "Custom Row"
        username = obj.username
        user = User.objects.get(username=username)
        if (user.has_perm('catalog.user_verified')):
            unverify_user_url = reverse('unverify_user', args=[username])
            url = f'<a class="button" href="{unverify_user_url}">Unverify</a>'
        else:
            verify_user_url = reverse('verify_user', args=[username])
            url = f'<a class="button" href="{verify_user_url}">Verify</a>'
        return format_html(url)
    custom_row.short_description = 'Toggle verification'

admin.site.register(User, CustomUserAdmin)

# Register the User model with your custom admin class