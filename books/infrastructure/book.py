from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound

from ..domain.book import Book, Isbn, BookRepository as BookRepositoryBase
from .database import Base

def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)

class BookDTO(Base):
    '''BookDTO is a DTO associated with Book entity'''

    __tablename__ = 'book'
    id: int | Column | None = Column(Integer, primary_key=True, autoincrement=True)
    isbn: str | Column = Column(String(17), unique=True, nullable=False)
    title: str | Column = Column(String, nullable=False)
    page: int | Column = Column(Integer, nullable=False)
    read_page: int | Column = Column(Integer, nullable=False, default=0)
    created_at: int | Column = Column(Integer, index=True, nullable=False)
    updated_at: int | Column = Column(Integer, index=True, nullable=False)

    def to_entity(self):
        return Book(
            id=self.id, #type: ignore
            isbn=Isbn(self.isbn), #type: ignore
            title=self.title, #type: ignore
            page=self.page, #type: ignore
            read_page=self.read_page, #type: ignore
            created_at=self.created_at, #type: ignore
            updated_at=self.updated_at, #type: ignore
        )

    @staticmethod
    def from_entity(book: Book) -> 'BookDTO':
        now = unixtimestamp()
        return BookDTO(
            id=book.id,
            isbn=book.isbn.value,
            title=book.title,
            page=book.page,
            read_page=book.read_page,
            created_at=now,
            updated_at=now,
        )

class BookRepository(BookRepositoryBase):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: str) -> Book | None:
        try:
            book_dto = self.session.query(BookDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise
        return book_dto.to_entity()

    def find_by_isbn(self, isbn: str) -> Book | None:
        try:
            book_dto = self.session.query(BookDTO).filter_by(isbn=isbn)
        except NoResultFound:
            return None
        except:
            raise
        return book_dto.to_entity()

    def create(self, book: Book) -> Book:
        book_dto = BookDTO.from_entity(book)
        try:
            self.session.add(book_dto)
            self.session.flush()
        except:
            raise
        return book_dto.to_entity()

    def update(self, book: Book):
        dto_to_update = BookDTO.from_entity(book)
        try:
            book_dto = self.session.query(BookDTO).filter_by(id=dto_to_update.id).one()
            book_dto.title = dto_to_update.title
            book_dto.page = dto_to_update.page
            book_dto.read_page = dto_to_update.read_page
            book_dto = dto_to_update.updated_at
        except:
            raise

    def delete_by_id(self, id: str):
        try:
            self.session.query(BookDTO).filter_by(id=id).delete()
        except:
            raise

    def get_all(self) -> List[Book]:
        try:
            book_dtos = (
                self.session.query(BookDTO)
                .order_by(BookDTO.updated_at)
                .limit(100)
                .all()
            )
        except:
            raise

        return list(map(lambda dto: dto.to_entity(), book_dtos))
