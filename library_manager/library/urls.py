from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-book/', views.add_book, name='add-book'),
    path('search-books/', views.search_books, name='search-books'),
    path('display-books/', views.display_books, name='display-books'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete-book'),
    path('update-status/<int:book_id>/', views.update_status, name='update-status'),
]
