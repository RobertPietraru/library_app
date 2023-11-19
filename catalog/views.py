import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render

from catalog.models import Book, BookInstance

# Create your views here.

def home(request):
    return render(request, 'home.html') ;


def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def books(request):
    query = request.GET.get('q', '')
    book_instances = BookInstance.objects.filter(
        Q(book__title__icontains=query) |
        Q(book__author__icontains=query) |
        Q(language__english_name__icontains=query) |
        Q(language__name__icontains=query)
    ) 

    context = {
        'book_instances': book_instances,
        'query': query
    }

    return render(request, 'books.html', context=context)

@staff_member_required
def report(request):
    query = request.GET.get('q', '')

    book_instances = BookInstance.objects.filter(
        Q(book__title__icontains=query) |
        Q(book__author__icontains=query) |
        Q(language__english_name__icontains=query) |
        Q(language__name__icontains=query)
    ) 

    context = {
        'book_instances': book_instances,
        'query': query
    }

    return render(request, 'report.html', context=context)

@staff_member_required
def download_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Language', 'Due Back', 'Status', 'Borrower'])

    for instance in BookInstance.objects.all():
        writer.writerow([
            instance.book.title,
            instance.book.author,
            instance.language.name,
            instance.due_back,
            instance.borrower.username if instance.borrower else '',
        ])

    return response

