from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances

class Book (models.Model) :
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)]) # type: ignore

class Language(models.Model):
    """The language of the books"""
    name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)

    class Meta:
        ordering = ['english_name']

    def __str__(self):
        return f'{self.name} ({self.english_name})'

class BookInstance(models.Model):
    """Un exemplar al cartii (nu-mi place cum suna instance in engleza)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # models.RESTRICT e ca sa nu poti sterge cartea daca mai exista exemplare in circulatie
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)

    language = models.ForeignKey( 'Language', on_delete=models.SET_NULL, null=True)
    # ii null cand cartea nu e in circulatie
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('u', 'Unavailbable'),
        ('o', 'Loaned'),
        ('a', 'Available'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='u',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.book.title} by {self.book.author} in {self.language}  ({self.id}) ' # type: ignore

