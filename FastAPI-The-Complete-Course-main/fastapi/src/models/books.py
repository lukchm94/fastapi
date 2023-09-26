class Book:
    def __init__(
        self, id: int, title: str, author: str, category: str, rating: int
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating


BOOKS = [
    Book(1, "Tennis", "Me", "IT", 10),
    Book(2, "Tennis 2", "You", "IT", 9),
    Book(3, "Tennis 3", "He", "IT", 8),
    Book(4, "Tennis 4", "He", "sport", 8),
    Book(5, "Tennis 5", "He", "sport", 8),
]
