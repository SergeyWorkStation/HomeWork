from logistics import Logistic, Delivery, Queue, Stack


def read_deliveries_by_file(filename: str) -> Logistic:
    with open(filename, 'r') as f:
        return Logistic([Delivery(line.split(', ')) for line in f.read().splitlines()])


def write_books_to_file(filename: str, books: Logistic) -> None:
    with open(filename, 'w') as f:
        f.write(repr(books))


def user_menu(filename: str) -> None:
    my_delivery = read_deliveries_by_file(filename)
    my_stack = Stack()
    my_queue = Queue()
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
                    print("Очередь пуста" if my_stack.is_empty() else my_stack)
                    input("Для продолжения нажмите Enter")

                if action == '2':
                    print(my_delivery)
                    deliveries_ids = map(int, input("\nНапишите порядковые номера доставок через пробел:").split())
                    for delivery_id in deliveries_ids:
                        my_stack.push(my_delivery[delivery_id-1])
                    input("Для продолжения нажмите Enter")

                if action == '3':
                    print(f"Очередная доставка: {my_stack.pop()} - обработана")
                    input("Для продолжения нажмите Enter")

                if action == '4':
                    break

        if action == '8':
            while True:
                print("""Система управления очередью доставки!

    Выберите действие:
    1.  Показать очередь
    2.  Добавить в очередь из списка доставок
    3.  Обработать очередную доставку
    4.  Выйти
                """)
                action = input("Введите номер действия:")

                if action == '1':
                    print("Список всех доставок в очереди:")
                    print("Очередь пуста" if my_queue.is_empty() else my_queue)
                    input("Для продолжения нажмите Enter")

                if action == '2':
                    print(my_delivery)
                    deliveries_ids = map(int, input("\nНапишите порядковые номера доставок через пробел:").split())
                    for delivery_id in deliveries_ids:
                        my_queue.enqueue(my_delivery[delivery_id - 1])
                    input("Для продолжения нажмите Enter")

                if action == '3':
                    print(f"Очередная доставка: {my_queue.dequeue()} - обработана")
                    input("Для продолжения нажмите Enter")

                if action == '4':
                    break

        if action == '10':
            approve = input("Перед завершением работы записать изменения в файл? да/нет:")
            if approve.lower() == 'да':
                write_books_to_file(input("Введите название файла:")+'.txt', my_delivery)
            break