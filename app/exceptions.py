class BookNotFoundError(Exception):
    pass

class DuplicateISBNError(Exception):
    pass

class InvalidBookDataError(Exception):
    pass

class BookNotAvailableError(Exception):
    pass

class LibraryFullError(Exception):
    pass
