from typing import cast, List
from pydantic import BaseModel, Field, validator
from ..domain.book import (Book,
    BookRepository,
    BookNotFoundError,
    BooksNotFoundError,
    BookIsbnAlreadyExistsError
)

class BookReadModel(BaseModel):
    '''BookReadModel represents data structure as a read model'''

    id: int = Field(example=1001)
    isbn: str = Field(example='978-0321125217')
    title: str = Field(
        example='Domain-Driven Design: Tackling Complexity in the Heart of Software'
    )
    page: int = Field(ge=0, example=320)
    read_page: int = Field(ge=0, example=120)
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    @staticmethod
    def from_entity(book: Book) -> 'BookReadModel':
        return BookReadModel(
            id=cast(int, book.id),
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            read_page=book.read_page,
            created_at=cast(int, book.created_at),
            updated_at=cast(int, book.updated_at),
        )

class BookCreateModel(BaseModel):
    '''BookCreateModel represents a write model to create a book.'''

    isbn: str = Field(example='978-0321125217')
    title: str = Field(
        example='Domain-Driven Design: Tackling Complexity in the Heart of Software'
    )
    page: int = Field(ge=0, example=320)

class BookUpdateModel(BaseModel):
    '''BookUpdateModel represents a write model to update a book'''

    title: str = Field(
        example='Domain-Driven Design: Tackling Complexity in the Heart of Software'
    )
    page: int = Field(ge=0, example=320)
    read_page: int = Field(ge=0, example=120)

    @validator('read_page')
    def _validate_read_page(cls, v, values):
        if 'page' in values and v > values['page']:
            raise ValueError(
                f'read_page must be between 0 and {values["page"]}'
            )
        return v

class ErrorMessageBookNotFound(BaseModel):
    detail: str = Field(example=BookNotFoundError.message)

class ErrorMessageBooksNotFoundError(BaseModel):
    detail: str = Field(example=BooksNotFoundError.message)

class ErrorMessageBookIsbnAlreadyExists(BaseModel):
    detail: str = Field(example=BookIsbnAlreadyExistsError.message)

class BookQuery:
    def __init__(self, book_repo: BookRepository):
        self.book_repo: BookRepository = book_repo

    def fetch_book_by_id(self, id: int) -> BookReadModel | None:
        try:
            book = self.book_repo.find_by_id(id)
            if book is None:
                raise BookNotFoundError
        except:
            raise
        return BookReadModel.from_entity(book)

    def fetch_books(self) -> List[BookReadModel]:
        try:
            books = self.book_repo.get_all()
        except:
            raise
        return list(map(lambda book: BookReadModel.from_entity(book), books))
