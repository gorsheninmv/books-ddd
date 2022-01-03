from typing import Iterator, List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from ..application.book import (
    BookReadModel,
    BookQuery,
    ErrorMessageBooksNotFoundError,
)

from ..domain.book import BookRepository

from ..infrastructure.database import SessionLocal
from ..infrastructure.book import BookRepository as BookRepositoryImpl

app = FastAPI()

def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def book_repo(session: Session = Depends(get_session)) -> BookRepository:
    return BookRepositoryImpl(session)

def book_query(book_repo: BookRepository = Depends(book_repo)) -> BookQuery:
    return BookQuery(book_repo)

@app.get(
    '/books',
    response_model=List[BookReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorMessageBooksNotFoundError,
        },
    }
)
async def get_books(
    book_query: BookQuery = Depends(book_query)
):
    try:
        books = book_query.fetch_books()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(books) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
