class Book:
    def __init__(self,title,author,isbn,category,publisher,publication_year,total_copies,available_copies,created_at=None,book_id=None):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.category=category
        self.publisher=publisher
        self.publication_year=publication_year
        self.total_copies=total_copies
        self.available_copies=available_copies
        self.created_at=created_at
        self.book_id=book_id