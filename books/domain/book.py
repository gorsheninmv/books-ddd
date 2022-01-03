import re
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

regex = r'978[-0-9]{10,15}'
pattern = re.compile(regex)

@dataclass(frozen=True)
class Isbn:
    '''Isbn represnts an ISBN code as a value object'''

    value: str

    def __init__(self, value: str):
        if pattern.match(value) is None:
            raise ValueError('ISBN should be a valid format')
        object.__setattr__(self, 'value', value)

class Book:
    '''Book represnts a collection of books as an entity'''

    def __init__(
        self,
        isbn: Isbn,
        title: str,
        page: int,
        read_page: int = 0,
        id: int | None = None,
        created_at: int | None = None,
        updated_at: int | None = None,
    ):
        self.id: int | None = id
        self.isbn: Isbn = isbn
        self.title: str = title
        self.page: int = page
        self.read_page: int = read_page
        self.created_at: int | None = created_at
        self.updated_at: int | None = updated_at

    def __eq__(self, o:object) -> bool:
        if isinstance(o, Book):
            if self.id is None or o.id is None:
                return False
            return self.id == o.id
        return False

    def is_already_read(self) -> bool:
        return self.page == self.read_page

class BookNotFoundError(Exception):
    message = 'The book you specified does not exist'

    def __str__(self):
        return BookNotFoundError.message

class BooksNotFoundError(Exception):
    message = 'No books were found'

    def __str__(self):
        return BooksNotFoundError.message

class BookIsbnAlreadyExistsError(Exception):
    message = 'The book with the ISBN code you specified already exists'

    def __str__(self):
        return BookIsbnAlreadyExistsError.message

class BookRepository(ABC):
    '''BookRepository defines a repository interface for Book entity'''

    @abstractmethod
    def create(self, book: Book) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_isbn(self, isbn: str) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, book: Book) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Book]:
        raise NotImplementedError
