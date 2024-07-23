from library.utils import Library


class LibraryManager:
    """Класс для управления библиотекой через консольный интерфейс."""

    def __init__(self, books_file='data/books.json'):
        self.library = Library(books_file=books_file)

    def run(self):
        """Запускает консольный интерфейс для управления библиотекой."""
        while True:
            print('\nМеню:')
            print('1. Добавить книгу')
            print('2. Удалить книгу')
            print('3. Поиск книг')
            print('4. Отображение всех книг')
            print('5. Изменение статуса книги')
            print('6. Выйти')

            match input('Выберите операцию: '):
                case '1':
                    try:
                        title = input('Введите название книги: ')
                        author = input('Введите автора книги: ')
                        year = input('Введите год издания книги: ')
                        self.library.add_book(title, author, year)
                    except (TypeError, ValueError) as error:
                        print(error)
                case '2':
                    try:
                        book_id = input('Введите id книги для удаления: ')
                        self.library.delete_book(book_id)
                    except (TypeError, ValueError) as error:
                        print(error)
                case '3':
                    keyword = input('Введите ключевое слово для поиска (название, автор или год): ')
                    founded_books = self.library.search_books(keyword)
                    for book in founded_books:
                        print(f'id: {book.id}, название: {book.title}, автор: {book.author}, '
                              f'год: {book.year}, статус: {book.status}')
                case '4':
                    self.library.display_books()
                case '5':
                    try:
                        book_id = input('Введите id книги для изменения статуса: ')
                        new_status = input("Введите новый статус книги ('в наличии' или 'выдана'): ")
                        self.library.change_status(book_id, new_status)
                    except (TypeError, ValueError) as error:
                        print(error)
                case '6':
                    break
                case _:
                    print('\nОшибка: неверный выбор. Пожалуйста, попробуйте снова.')
