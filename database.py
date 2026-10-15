import psycopg
import os
from dotenv import load_dotenv
load_dotenv()
class Database:
    def __init__(self):
        self.connection=psycopg.connect(
            host="localhost",
            dbname="library management system",
            password=os.getenv("DB_PASSWORD"),
            port=5432,
            user="postgres"
        )
        self.cursor=self.connection.cursor()

    #Book
    def addBook(self,book):
        try:
            self.cursor.execute(
                "select category_id from categories" \
                " where category=%s",(book.category,)
            )
            category=self.cursor.fetchone()
            if category is None:
                self.cursor.execute(
                    "insert into categories(category)" \
                    " values(%s) returning category_id",(book.category,)
                )
                category_id=self.cursor.fetchone()[0]
            else:
                category_id=category[0]
            self.cursor.execute(
                "insert into books(title,author,isbn,category_id,publisher,publication_year,total_copies,available_copies)" \
                " values(%s,%s,%s,%s,%s,%s,%s,%s)",(book.title,book.author,book.isbn,category_id,book.publisher,book.publication_year,book.total_copies,book.available_copies)
            )
            
            self.connection.commit()
            return True
        except psycopg.errors.NotNullViolation as e:
            self.connection.rollback()
            return f"{e.diag.column_name} is missing"
        except psycopg.errors.CheckViolation as e:
            self.connection.rollback()
            return "Total copies must be greater than 0, and available copies cannot exceed total copies."

        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return False

    def viewAllBook(self):
        try:
            self.cursor.execute(
                "select b.book_id,b.title,b.author,b.isbn,c.category,b.publisher,b.publication_year,b.total_copies,b.available_copies" \
                " from books b" \
                " join categories c on c.category_id=b.category_id"
            )
            rows=self.cursor.fetchall()
            return rows
        except psycopg.Error as e:
            print(e)
            return None

    def searchBookId(self,book_id):
        try:
            self.cursor.execute(
                "select * from books" \
                " where book_id=%s",(book_id,)
            )
            book=self.cursor.fetchone()
            return book
        except psycopg.Error as e:
            print(e)
            return None

    def searchBookTitle(self,title):
        try:
            self.cursor.execute(
                "select * from books" \
                " where lower(title)=%s",(title.lower(),)
            )
            book=self.cursor.fetchone()
            return book
        except psycopg.Error as e:
            print(e)
            return None

    def updateBook(self,book):
        try:
            self.cursor.execute(
                "select category_id from categories" \
                " where category=%s",(book.category,)
            )
            category=self.cursor.fetchone()
            if category is None:
                self.cursor.execute(
                    "insert into categories(category)" \
                    " values(%s) returning category_id",(book.category,)
                )
                category_id=self.cursor.fetchone()[0]
            else:
                category_id=category[0]
            self.cursor.execute(
                "update books" \
                " set title=%s,author=%s,isbn=%s,category_id=%s,publisher=%s,publication_year=%s,total_copies=%s,available_copies=%s" \
                " where book_id=%s",(book.title,book.author,book.isbn,category_id,book.publisher,book.publication_year,book.total_copies,book.available_copies,book.book_id)
            )
            self.connection.commit()
            return True
        except psycopg.errors.NotNullViolation as e:
            self.connection.rollback()
            return f"{e.diag.column_name} is missing"
        except psycopg.errors.CheckViolation as e:
            self.connection.rollback()
            return "Total copies must be greater than 0, and available copies cannot exceed total copies."

        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return False


    def deleteBook(self,book_id):
        try:
            self.cursor.execute(
                "delete from books" \
                " where book_id=%s",(book_id,)
            )
            self.connection.commit()
            return True
        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return False
        

    def checkAvailableCopies(self):
        try:
            self.cursor.execute(
                "select book_id,title,author,available_copies from books" \
                " where available_copies>0"
            )
            rows=self.cursor.fetchall()
            return rows
        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return None


    #Member
    
    def registerMember(self,member):
        try:
            self.cursor.execute(
                "insert into members(name,email,phone,address)" \
                " values(%s,%s,%s,%s)",(member.name,member.email,member.phone,member.address)
            )
            self.connection.commit()
            return True
        except psycopg.errors.NotNullViolation as e:
            self.connection.rollback()
            return f"{e.diag.column_name} is missing."
        except psycopg.errors.CheckViolation as e:
            self.connection.rollback()
            return f"Email is invalid."
        except psycopg.errors.UniqueViolation as e:
            self.connection.rollback()
            return f"Email already exist."
        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return False

    def viewAllMember(self):
        try:
            self.cursor.execute(
                "select * from members"
            )
            rows=self.cursor.fetchall()
            return rows
        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return None
    def searchMemByID(self,member_id):
        try:
            self.cursor.execute(
                "select * from members" \
                " where member_id=%s",(member_id,)
            )
            member=self.cursor.fetchone()
            return member
        except psycopg.Error as e:
            self.connection.rollback()
            print(e)
            return "Internal server error"

    def searchMemByName(self,name):
        self.cursor.execute(
            "select * from members" \
            " where name=%s",(name,)
        )
        member=self.cursor.fetchall()
        return member
    
    def searchMemByEmail(self,email):
        self.cursor.execute(
            "select * from members" \
            " where email=%s",(email,)
        )
        member=self.cursor.fetchone()
        return member 

    def updateMember(self,member):
        self.cursor.execute(
            "update members" \
            " set name=%s, email=%s, phone=%s, address=%s" \
            " where member_id=%s",(member.name,member.email,member.phone,member.address,member.member_id)
        )
        self.connection.commit()
        return True

    def deleteMember(self,member_id):
        self.cursor.execute(
            "delete from members" \
            " where member_id=%s",(member_id,)
        )
        self.connection.commit()
        return True

    #Borrow

    def borrowBook(self,borrow):
        self.cursor.execute(
            "select available_copies from books" \
            " where book_id=%s",(borrow.book_id,)
        )
        book=self.cursor.fetchone()
        if book is None or book[0]<=0:
            return False
        self.cursor.execute(
            "insert into borrows(book_id,member_id,due_date)" \
            " values(%s,%s,current_timestamp+interval '14 days')",(borrow.book_id,borrow.member_id)

        )
        self.cursor.execute(
            "update books" \
            " set available_copies=available_copies-1" \
            " where book_id=%s",(borrow.book_id,)
        )
        self.connection.commit()
        return True

    def returnBook(self,borrowing_id):
        self.cursor.execute(
            "update borrows" \
            " set return_date=current_timestamp" \
            " where borrowing_id=%s and return_date is null returning book_id",(borrowing_id,)
        )
        book=self.cursor.fetchone()
        if book is None:
            return False
        book_id=book[0]
        self.cursor.execute(
            "update books" \
            " set available_copies=available_copies+1" \
            " where book_id=%s",(book_id,)
        )
        self.connection.commit()
        return True

    def borrowHistory(self):
        self.cursor.execute(
            "select * from borrows"
        )
        borrows=self.cursor.fetchall()
        return borrows

    def currentBorrow(self):
        self.cursor.execute(
            "select * from borrows" \
            " where return_date is null"
        )
        borrows=self.cursor.fetchall()
        return borrows

    def currentOverdue(self):
        self.cursor.execute(
            "select * from borrows" \
            " where return_date is null" \
            " and due_date<current_timestamp"
        )
        borrows=self.cursor.fetchall()
        return borrows

    def overdueHistory(self):
        self.cursor.execute(
            "select * from borrows" \
            " where return_date>due_date"
        )
        borrows=self.cursor.fetchall()
        return borrows
    
    #category

    def viewAllCategory(self):
        self.cursor.execute(
            "select * from categories"
        )
        categories=self.cursor.fetchall()
        return categories
           
                                                            
