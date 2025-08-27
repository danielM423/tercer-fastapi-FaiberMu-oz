def test_create_book_success(client):
    response = client.post("/books", json={
        "title": "FastAPI for Beginners",
        "author": "Tech Writer",
        "isbn": "978-1234567890",
        "year": 2020,
        "rating": 4.5,
        "tags": ["python", "fastapi"],
        "price": 25.0
    })
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_create_book_duplicate_isbn(client):
    # Crear primero
    client.post("/books", json={
        "title": "Book One",
        "author": "Author A",
        "isbn": "978-1234567890",
        "year": 2010,
        "rating": 4.0,
        "tags": [],
        "price": 15.0
    })
    # Intentar duplicado
    response = client.post("/books", json={
        "title": "Book Two",
        "author": "Author B",
        "isbn": "978-1234567890",
        "year": 2015,
        "rating": 4.0,
        "tags": [],
        "price": 20.0
    })
    assert response.status_code == 400
