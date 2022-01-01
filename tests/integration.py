import unittest
from books.infrastructure.database import SessionLocal
from books.infrastructure.book import BookRepository
from books.domain.book import Book, Isbn

class TestBookRepository(unittest.TestCase):
    def test_create_new_book(self):
        with SessionLocal() as session:
            book_repo = BookRepository(session)
            book = Book(
                isbn=Isbn('9781111111112'),
                title='test book',
                page=10,
                read_page=10
            )
            book = book_repo.create(book)
            print(book.id)
            self.assertTrue(book.id is not None)

if __name__ == '__main__':
    unittest.main()
