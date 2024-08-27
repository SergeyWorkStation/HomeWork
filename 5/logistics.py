from __future__ import annotations
import algorithms as alg


class Delivery:

    def __init__(self, delivery_list: list[str]) -> None:
        self.__number = int(delivery_list[0])
        self.__departure = delivery_list[1]
        self.__destination = delivery_list[2]
        self.__weight = int(delivery_list[3])
        self.__time = int(delivery_list[4])

    def __repr__(self) -> str:
        return f'{self.__number}, {self.__departure}, {self.__destination}, {self.__weight}, {self.__time}'

    def __str__(self) -> str:
        return (f'Delivery № {self.__number}, departure point: {self.__departure}, destination: {self.__destination}, '
                f'cargo weight: {self.__weight} kg, delivery time: {self.__time} days')

    @property
    def weight(self):
        return self.__weight

    @property
    def time(self):
        return self.__time

    @property
    def number(self):
        return self.__number


class Logistic:

    def __init__(self, args: list[Delivery]) -> None:
        self.__delivery_list = args

    def __repr__(self) -> str:
        return '\n'.join([f"{repr(delivery)}" for delivery in self.__delivery_list])

    def __str__(self) -> str:
        return '\n'.join([f"{i+1}\t {delivery}" for i, delivery in enumerate(self.__delivery_list)])

    def __getitem__(self, item):
        return self.__delivery_list[item]

    def search_by_number(self, delivery_num: str) -> Logistic | None:
        delivery_list = [delivery for delivery in self.__delivery_list if delivery.number == int(delivery_num)]
        return Logistic(delivery_list) if delivery_list else None

    def search_by_time(self, delivery_time: str) -> Logistic | None:
        sorted_list = self.sort_by_time()
        delivery_index = alg.binary_search(sorted_list.__delivery_list, int(delivery_time))
        return Logistic([sorted_list.__delivery_list[delivery_index]]) if delivery_index != -1  else None

    def sort_by_weight(self) -> Logistic:
        return Logistic(alg.merge_sort(self.__delivery_list.copy()))

    def sort_by_time(self) -> Logistic:
        return Logistic(alg.quick_sort(self.__delivery_list.copy()))

    def sort_by_number(self) -> Logistic:
        return Logistic(alg.heap_sort(self.__delivery_list.copy()))


class Queue:
    def __init__(self) -> None:
        self.__queue = []

    def enqueue(self, item: any) -> None:
        self.__queue.append(item)

    def dequeue(self) -> any:
        if not self.is_empty():
            return self.__queue.pop(0)
        raise IndexError("dequeue from empty queue")

    def is_empty(self) -> bool:
        return len(self.__queue) == 0

    def size(self) -> int:
        return len(self.__queue)

    def __str__(self) -> str:
        return '\n'.join([f"{i+1}\t {delivery}" for i, delivery in enumerate(self.__queue)])


class Stack:
    def __init__(self) -> None:
        self.__items = []

    def is_empty(self) -> bool:
        return len(self.__items) == 0

    def push(self, item: any) -> None:
        self.__items.append(item)

    def pop(self) -> any:
        if not self.is_empty():
            return self.__items.pop()
        raise IndexError("удаление из пустого стека")

    def peek(self) -> any:
        if not self.is_empty():
            return self.__items[-1]
        raise IndexError("получение из пустого стека")

    def size(self) -> int:
        return len(self.__items)

    def __str__(self) -> str:
        return '\n'.join([f"{i+1}\t {delivery}" for i, delivery in enumerate(self.__items)])