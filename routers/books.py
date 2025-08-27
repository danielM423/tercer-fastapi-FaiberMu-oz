from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.exceptions import *

router = APIRouter(prefix="/books", tags=["books"])

books_db = []  # simulación en memoria
borrowed_books = []

MAX_BORROWED = 10

@router.get("/search")
def search_books(q: Optional[str] = None) -> List[dict]:
    if not q or len(q) < 2:
        raise InvalidBookDataError("La búsqueda debe tener al menos 2 caracteres")
    return [b for b in books_db if q.lower() in b["title"].lower()]

@router.post("/{book_id}/borrow")
def borrow_book(book_id: int):
    book = next((b for b in books_db if b["id"] == book_id), None)
    if not book:
        raise BookNotFoundError(f"Book with ID {book_id} not found")
    if not book["is_available"]:
        raise BookNotAvailableError("Book not available")
    if len(borrowed_books) >= MAX_BORROWED:
        raise LibraryFullError("Library borrow limit reached")

    book["is_available"] = False
    borrowed_books.append(book)
    return {"success": True, "message": "Book borrowed successfully"}

@router.post("/{book_id}/return")
def return_book(book_id: int):
    book = next((b for b in borrowed_books if b["id"] == book_id), None)
    if not book:
        raise BookNotFoundError("This book is not currently borrowed")
    book["is_available"] = True
    borrowed_books.remove(book)
    return {"success": True, "message": "Book returned successfully"}
