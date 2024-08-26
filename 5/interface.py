from logistics import Logistic, Delivery


def read_deliveries_by_file(filename: str) -> Logistic:
    with open(filename, 'r') as f:
        return Logistic([Delivery(line.split(', ')) for line in f.read().splitlines()])


def write_books_to_file(filename: str, books: Logistic) -> None:
    with open(filename, 'w') as f:
        f.write(repr(books))


def user_menu(filename: str) -> None:
    my_delivery = read_deliveries_by_file(filename)
    while True:
        print("""Добро пожаловать в систему управления доставкой!

    Выберите действие:
    1.  Показать все доставки
    2.  Сортировать доставки по весу
    3.  Сортировать доставки по времени
    4.  Сортировать доставки по номеру
    5.  Найти доставку по номеру
    6.  Найти доставку по времени
    7.  Срочные доставки (стек)
    8.  Обычная очередь 
    9.  Удалить книгу
    10. Выйти
    """)
        action = input("Введите номер действия:")
        if action == '1':
            print("Список всех доставок:")
            print(my_delivery)
            input("Для продолжения нажмите Enter")

        if action == '2':
            print("Список доставки отсортированный по весу:")
            print(my_delivery.sort_by_weight())
            input("Для продолжения нажмите Enter")

        if action == '3':
            print("Список доставки отсортированный по времени:")
            print(my_delivery.sort_by_time())
            input("Для продолжения нажмите Enter")

        if action == '4':
            print("Список доставки отсортированный по весу:")
            print(my_delivery.sort_by_number())
            input("Для продолжения нажмите Enter")

        if action == '5':
            number = input("Введите номер доставки:")
            deliveries = my_delivery.search_by_number(number)
            print(deliveries if deliveries else "Доставка не найдена")
            input("Для продолжения нажмите Enter")

        if action == '6':
            time = input("Введите количество дней доставки:")
            deliveries = my_delivery.search_by_time(time)
            print(deliveries if deliveries else "Доставка не найдена")
            input("Для продолжения нажмите Enter")

        if action == '7':
            while True:
                print("""Система управления быстрой очередью доставки!

                Выберите действие:
                1.  Показать очередь
                2.  Добавить в очередь из списка доставок
                3.  Обработать очередную доставку
                4.  Выйти
                """)
                action = input("Введите номер действия:")

                if action == '1':
                    print("Список всех доставок в очереди:")
                    print(my_delivery)
                    input("Для продолжения нажмите Enter")

                if action == '2':
                    print("Список доставки отсортированный по весу:")
                    print(my_delivery.sort_by_weight())
                    input("Для продолжения нажмите Enter")

                if action == '3':
                    print("Список доставки отсортированный по времени:")
                    print(my_delivery.sort_by_time())
                    input("Для продолжения нажмите Enter")

                if action == '4':
                    break

        if action == '8':
            print(my_delivery)
            try:
                book_id = int(input("Введите книги которую необходимо удалить :"))
                # my_delivery.delete_book(book_id - 1)
                print("Книга удалена из библиотеки")
            except:
                print("Не удалось удалить книгу из библиотеки")
            finally:
                input("Для продолжения нажмите Enter")

        if action == '9':
            approv = input("Перед завершением работы записать изменения в файл? да/нет:")
            if approv.lower() == 'да':
                write_books_to_file(input("Введите название файла:")+'.txt', my_delivery)
            break