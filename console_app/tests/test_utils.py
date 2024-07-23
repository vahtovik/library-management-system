import unittest
from unittest.mock import patch
import json
import tempfile
import os

from library.manager import LibraryManager
from library.utils import Book, Library


class TestBook(unittest.TestCase):
    def test_to_dict(self):
        book = Book(1, 'Title', 'Author', 2000, 'в наличии')
        self.assertEqual(book.to_dict(), {
            'id': 1,
            'title': 'Title',
            'author': 'Author',
            'year': 2000,
            'status': 'в наличии'
        })

    def test_from_dict(self):
        book_dict = {
            'id': 1,
            'title': 'Title',
            'author': 'Author',
            'year': 2000,
            'status': 'в наличии'
        }
        book = Book.from_dict(book_dict)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, 'Title')
        self.assertEqual(book.author, 'Author')
        self.assertEqual(book.year, 2000)
        self.assertEqual(book.status, 'в наличии')


class TestLibrary(unittest.TestCase):

    def setUp(self):
        # Создаем временный каталог и файл books.json
        self.test_dir = tempfile.TemporaryDirectory()
        self.books_file_path = os.path.join(self.test_dir.name, 'books.json')

        self.test_books_data = [
            {
                'id': 1,
                'title': 'Title1',
                'author': 'Author1',
                'year': 2000,
                'status': 'в наличии'
            },
            {
                'id': 2,
                'title': 'Title2',
                'author': 'Author2',
                'year': 2001,
                'status': 'выдана'
            }
        ]

        # Пишем тестовые данные в файл books.json
        with open(self.books_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.test_books_data, file, indent=4, ensure_ascii=False)

        # Создаем экземпляр библиотеки с временным файлом
        self.library = Library(books_file=self.books_file_path)

    def tearDown(self):
        # Удаляем временный каталог и все его содержимое после каждого теста
        self.test_dir.cleanup()

    def test_load_books(self):
        books = self.library.load_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, 'Title1')
        self.assertEqual(books[1].author, 'Author2')

    def test_save_books(self):
        new_book = Book(3, 'Title3', 'Author3', 2002, 'в наличии')
        self.library.books.append(new_book)
        self.library.save_books()

        with open(self.books_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(len(data), 3)
            self.assertEqual(data[2]['title'], 'Title3')

    def test_generate_id(self):
        self.assertEqual(self.library.generate_id(), 3)

    def test_add_book(self):
        self.library.add_book('Title3', 'Author3', '2002')
        self.assertEqual(len(self.library.books), 3)
        self.assertEqual(self.library.books[-1].title, 'Title3')
        with self.assertRaises(TypeError):
            self.library.add_book('Title4', 'Author4', 'year')
        with self.assertRaises(ValueError):
            self.library.add_book('Title4', 'Author4', '1000')

    def test_delete_book(self):
        self.library.delete_book('1')
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].id, 2)
        with self.assertRaises(TypeError):
            self.library.delete_book('book_id')
        with self.assertRaises(ValueError):
            self.library.delete_book('3')

    def test_change_status(self):
        self.library.change_status('1', 'выдана')
        self.assertEqual(self.library.books[0].status, 'выдана')
        with self.assertRaises(TypeError):
            self.library.change_status('book_id', 'выдана')
        with self.assertRaises(ValueError):
            self.library.change_status('1', 'status')
        with self.assertRaises(ValueError):
            self.library.change_status('3', 'выдана')

    def test_search_books(self):
        results = self.library.search_books('Title1')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Title1')

    def test_is_book_presented(self):
        presented_book = self.library.is_book_presented(1)
        self.assertEqual(presented_book, True)
        not_presented_book = self.library.is_book_presented(3)
        self.assertEqual(not_presented_book, False)


class TestLibraryManager(unittest.TestCase):

    def setUp(self):
        # Создаем временный каталог и файл books.json
        self.test_dir = tempfile.TemporaryDirectory()
        self.books_file_path = os.path.join(self.test_dir.name, 'books.json')

        self.manager = LibraryManager(books_file=self.books_file_path)

    @patch('builtins.input', side_effect=['1', 'Title', 'Author', '2000', '6'])
    @patch('builtins.print')
    def test_run(self, mock_print, mock_input):
        with patch.object(Library, 'add_book', wraps=self.manager.library.add_book) as mock_add:
            self.manager.run()
            mock_add.assert_called_once_with('Title', 'Author', '2000')
            mock_print.assert_any_call('\nКнига успешно добавлена!')


if __name__ == '__main__':
    unittest.main()
