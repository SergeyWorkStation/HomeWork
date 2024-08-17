from __future__ import annotations
import sorting as srt


class Book:

    def __init__(self, book_str: list[str]) -> None:
        self.__title = book_str[0]
        self.__author = book_str[1]
        self.__year = int(book_str[2])

    def __repr__(self) -> str:
        return f'{self.__title}, {self.__author}, {self.__year}'

    def __str__(self) -> str:
        return f'"{self.__title}" by {self.__author} ({self.__year})'

    @property
    def author(self):
        return self.__author

    @property
    def title(self):
        return self.__title

    @property
    def year(self):
        return self.__year


class Library:

    def __init__(self, args: list[Book]) -> None:
        self.__book_list = args

    def __repr__(self) -> str:
        return '\n'.join([f"{repr(book)}" for book in self.__book_list])

    def __str__(self) -> str:
        return '\n'.join([f"{i+1}\t {book}" for i, book in enumerate(self.__book_list)])

    def insert(self, book: str) -> None:
        self.__book_list.append(Book(book.split(', ')))

    def search_by_author(self, book_author: str) -> Library | None:
        book_list = [book for book in self.__book_list if book.author == book_author]
        return Library(book_list) if book_list else None

    def search_by_title(self, book_title: str) -> Library | None:
        book_list = [book for book in self.__book_list if book.title == book_title]
        return Library(book_list) if book_list else None

    def delete_book(self, book_id: int) -> None:
        if 0 <= book_id < len(self.__book_list):
            self.__book_list.pop(book_id)

    def sort_books_by_title(self) -> Library:
        arr = self.__book_list.copy()
        return Library(srt.quick_sort(arr))

    def sort_books_by_author(self) -> Library:
        arr = self.__book_list.copy()
        return Library(srt.merge_sort(arr))

    def sort_books_by_year(self) -> Library:
        arr = self.__book_list.copy()
        return Library(srt.heap_sort(arr))