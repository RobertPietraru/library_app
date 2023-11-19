import csv
from datetime import timedelta
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Book, BookInstance

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html') ;


@login_required
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


@login_required
def my_books(request):
    query = request.GET.get('q', '')
    book_instances = BookInstance.objects.filter(
        Q(book__title__icontains=query) |
        Q(book__author__icontains=query) |
        Q(language__english_name__icontains=query) |
        Q(language__name__icontains=query),
        borrower=request.user,
    ) 

    context = {
        'book_instances': book_instances,
        'query': query
    }

    return render(request, 'my_books.html', context=context)

@login_required
def return_book(request, id):
    book_instance = get_object_or_404(BookInstance, id=id)

    book_instance.due_back = None
    book_instance.status = 'a'  
    book_instance.borrower = None
    book_instance.save()

    return redirect('my_books')
@login_required
def borrow_book(request, id):
    print('yes');
    book_instance = get_object_or_404(BookInstance, id=id)

    # la noi la biblioteca ai 2 saptmanai pana trebuie sa aduci cartea
    book_instance.due_back = datetime.datetime.now() + timedelta(days=14)
    book_instance.status = 'o'  
    book_instance.borrower = request.user
    book_instance.save()

    return redirect('my_books')
    
@login_required
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

