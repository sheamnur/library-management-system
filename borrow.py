class Borrow:
    def __init__(self,book_id,member_id,borrowing_id=None,borrow_date=None,due_date=None,return_date=None):
        self.book_id=book_id
        self.member_id=member_id
        self.borrowing_id=borrowing_id
        self.borrow_date=borrow_date
        self.due_date=due_date
        self.return_date=return_date