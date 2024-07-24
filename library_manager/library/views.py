from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookForm, UpdateStatusForm, SearchForm
from .models import Book


def index(request):
    return render(request, 'library/index.html')


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library:index')
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})


def search_books(request):
    form = SearchForm()
    books = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            books = Book.objects.filter(title__icontains=keyword) | \
                    Book.objects.filter(author__icontains=keyword) | \
                    Book.objects.filter(year__icontains=keyword)

    return render(request, 'library/search_books.html', {'form': form, 'books': books})


def display_books(request):
    books = Book.objects.all()
    context = {
        'books': books,
    }

    return render(request, 'library/display_books.html', context=context)


def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('library:index')
    return render(request, 'library/delete_book.html', {'book': book})


def update_status(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library:index')
    else:
        form = UpdateStatusForm(instance=book)
    return render(request, 'library/update_status.html', {'form': form, 'book': book})
