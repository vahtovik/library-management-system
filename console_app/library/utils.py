import json
import os
from datetime import datetime
from typing import Self


class Book:
    """Класс, представляющий книгу в библиотеке."""

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = 'в наличии'):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """Преобразует объект книги в словарь."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Создает объект книги из словаря."""
        return cls(data['id'], data['title'], data['author'], data['year'], data['status'])


class Library:
    """Класс, представляющий библиотеку книг."""

    ALLOWED_STATUSES = ('в наличии', 'выдана')
    MIN_YEAR = 1450
    MAX_YEAR = datetime.now().year

    def __init__(self, books_file='data/books.json'):
        self.books_file = books_file
        self.books = self.load_books()

    def load_books(self) -> list:
        """Загружает книги из файла JSON."""
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r', encoding='utf-8') as file:
                return [Book.from_dict(book) for book in json.load(file)]
        return []

    def save_books(self) -> None:
        """Сохраняет книги в файл JSON."""
        with open(self.books_file, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4, ensure_ascii=False)

    def generate_id(self) -> int:
        """Генерирует уникальный идентификатор для новой книги."""
        if self.books:
            return max(book.id for book in self.books) + 1
        return 1

    def add_book(self, title: str, author: str, year: str) -> None:
        """Добавляет книгу в библиотеку."""
        if not year.isdigit():
            raise TypeError('\nОшибка: год должен быть числом!')

        year = int(year)
        if year < self.MIN_YEAR or year > self.MAX_YEAR:
            raise ValueError(f'\nОшибка: год издания должен быть в диапазоне от {self.MIN_YEAR} до {self.MAX_YEAR}!')

        new_book = Book(self.generate_id(), title, author, year)
        self.books.append(new_book)
        self.save_books()
        print('\nКнига успешно добавлена!')

    def delete_book(self, book_id: str) -> None:
        """Удаляет книгу из библиотеки по идентификатору."""
        if not book_id.isdigit():
            raise TypeError('\nОшибка: id должно быть числом!')

        book_id = int(book_id)
        if not self.is_book_presented(book_id):
            raise ValueError('\nОшибка: книги с таким id не существует!')

        self.books = [book for book in self.books if book.id != book_id]
        self.save_books()
        print('\nКнига успешно удалена!')

    def change_status(self, book_id: str, new_status: str) -> None:
        """Изменяет статус книги."""
        if not book_id.isdigit():
            raise TypeError('\nОшибка: id должно быть числом!')

        if new_status not in self.ALLOWED_STATUSES:
            raise ValueError(f'\nОшибка: неверный статус.')

        book_id = int(book_id)
        if not self.is_book_presented(book_id):
            raise ValueError('\nОшибка: книги с таким id не существует!')

        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                break

        print('\nСтатус книги успешно изменен!')

    def search_books(self, keyword: str) -> list[Book]:
        """Ищет книги по ключевому слову."""
        founded_books = [book for book in self.books if (keyword.strip().lower() in book.title.lower() or
                                                         keyword.strip().lower() in book.author.lower() or
                                                         keyword.strip().lower() in str(book.year))]
        if founded_books:
            print('\nРезультаты поиска:')
            return founded_books
        else:
            print('Поиск не дал результатов.')

    def display_books(self) -> None:
        """Отображает все книги в библиотеке."""
        print()
        if self.books:
            print('Книги в библиотеке:')
            for book in self.books:
                print(f'id: {book.id}, название: {book.title}, автор: {book.author}, '
                      f'год: {book.year}, статус: {book.status}')
        else:
            print('Библиотека пуста!')

    def is_book_presented(self, book_id: int) -> bool:
        """Проверяет присутствует ли книга в библиотеке."""
        for book in self.books:
            if book.id == book_id:
                return True

        return False
