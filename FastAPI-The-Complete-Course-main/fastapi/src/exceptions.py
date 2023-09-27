from datetime import datetime


class RatingError(Exception):
    def __init__(self, rating: int) -> None:
        super().__init__(f"Rating of {rating} not allowed. Max rating is 10")


class YearError(Exception):
    def __init__(self, year: int) -> None:
        super().__init__(
            f"{year} not allowed choose year between 2000 and {datetime.now().year}"
        )
