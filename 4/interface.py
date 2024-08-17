from library import Library, Book


def read_books_by_file(filename: str) -> Library:
    with open(filename, 'r') as f:
        return Library([Book(line.split(', ')) for line in f.read().splitlines()])


def write_books_to_file(filename: str, books: Library) -> None:
    with open(filename, 'w') as f:
        f.write(repr(books))


def user_menu(filename: str) -> None:
    my_lib = read_books_by_file(filename)
    while True:
        print("""Добро пожаловать в систему управления библиотекой!

    Выберите действие:
    1. Показать все книги
    2. Сортировать книги по названию
    3. Сортировать книги по автору
    4. Сортировать книги по году издания
    5. Найти книгу по названию
    6. Найти книгу по автору
    7. Добавить книгу
    8. Удалить книгу
    9. Выйти
    """)
        action = input("Введите номер действия:")
        if action == '1':
            print("Список всех книг:")
            print(my_lib)
            input("Для продолжения нажмите Enter")

        if action == '2':
            print("Список книг отсортированных по названию:")
            print(my_lib.sort_books_by_title())
            input("Для продолжения нажмите Enter")

        if action == '3':
            print("Список книг отсортированных по автору:")
            print(my_lib.sort_books_by_author())
            input("Для продолжения нажмите Enter")

        if action == '4':
            print("Список книг отсортированных по году издания:")
            print(my_lib.sort_books_by_year())
            input("Для продолжения нажмите Enter")

        if action == '5':
            title = input("Введите название книги:")
            books = my_lib.search_by_title(title)
            print(books if books else "Книги не найдены")
            input("Для продолжения нажмите Enter")

        if action == '6':
            author = input("Введите автора книги:")
            books = my_lib.search_by_author(author)
            print(books if books else "Книги не найдены")
            input("Для продолжения нажмите Enter")

        if action == '7':
            book = input("Введите информацию о книги в формате \nНазвание книги, Автор, год издания \n:")
            try:
                my_lib.insert(book)
                print("Книга добавлена в библиотеку")
            except:
                print("Не удалось добавить в библиотеку")
            finally:
                input("Для продолжения нажмите Enter")

        if action == '8':
            print(my_lib)
            try:
                book_id = int(input("Введите книги которую необходимо удалить :"))
                my_lib.delete_book(book_id - 1)
                print("Книга удалена из библиотеки")
            except:
                print("Не удалось удалить книгу из библиотеки")
            finally:
                input("Для продолжения нажмите Enter")

        if action == '9':
            approv = input("Перед завершением работы записать изменения в файл? да/нет:")
            if approv.lower() == 'да':
                write_books_to_file(input("Введите название файла:")+'.txt', my_lib)
            break