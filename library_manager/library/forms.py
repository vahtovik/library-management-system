from datetime import datetime

from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'status']
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'year': 'Год издания',
            'status': 'Статус'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=Book.STATUS_CHOICES, attrs={'class': 'form-control'}),
        }

    def clean_year(self):
        year = self.cleaned_data.get('year')
        min_year = 1450
        max_year = datetime.now().year
        if year < min_year or year > max_year:
            raise forms.ValidationError(f'Год издания должен быть в диапазоне от {min_year} до {max_year}.')
        return year


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, label='Ключевое слово',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['status']
        labels = {
            'status': 'Статус книги',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
