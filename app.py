from flask import Flask,jsonify,request
from book import Book
from member import Member
from borrow import Borrow
from database import Database
database=Database()


app=Flask(__name__)


#Books


@app.route("/books",methods=["get"])
def viewBook():
    Books=database.viewAllBook()
    if Books is None:
        return jsonify({
            "error":"Books could not be retreived."
        })
    return jsonify(Books)

@app.route("/books",methods=["post"])
def addBook():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data is required."
        })

    required_field={
        "title":str,
        "author":str,
        "isbn":str,
        "category":str,
        "publisher":str,
        "publication_year":int,
        "total_copies":int,
        "available_copies":int,
    }
    for field in required_field:
        if field not in data:
            return jsonify({
                "error":f"{field} is required."
            })

    for key,value in required_field.items():
        if not isinstance(data[key],value):
            return jsonify({
                "error":f"{key} must be {value.__name__}"
            })

    book=Book(
        data["title"],data["author"],data["isbn"],data["category"],data["publisher"],data["publication_year"],data["total_copies"],data["available_copies"]
    )
    result=database.addBook(book)
    if result:
        return jsonify({
            "message":"Book add successfully."
            })

@app.route("/books/<book_id>",methods=["patch"])
def updateBook(book_id):
    books=database.viewAllBook()
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data is required."
        })
    
    required_field={
        "title":str,
        "author":str,
        "isbn":str,
        "category":str,
        "publisher":str,
        "publication_year":int,
        "total_copies":int,
        "available_copies":int,
    }
    for key in data:
        if key not in required_field:
            return jsonify({
                "error":f"{key} is not allow."
            })

    for key,value in required_field.items():
        if key in data:
            if not isinstance(data[key],value):
                return jsonify({
                    "error":f"{key} must be {value.__name__}"
                })

    

    if books is None:
        return jsonify({
            "error":"Books could not be retreived."
        })
    elif not books:
        return jsonify({
            "error":"No books in the record."
        })
    else:
        book=None
        for row in books:
            if row[0]==int(book_id):
                book={
                    "book_id":row[0],
                    "title":row[1],
                    "author":row[2],
                    "isbn":row[3],
                    "category":row[4],
                    "publisher":row[5],
                    "publication_year":row[6],
                    "total_copies":row[7],
                    "available_copies":row[8]
                }
            
                for key,value in data.items():
                    book[key]=value
                break
        if book is None:
            return jsonify({
                "error":"Book not found."
            })
        

    book=Book(
        book["title"],book["author"],book["isbn"],book["category"],book["publisher"],book["publication_year"],book["total_copies"],book["available_copies"],book_id=book["book_id"]
    )
    result=False
    result=database.updateBook(book)
    if result:
        return jsonify({
            "message":"Book update successfully."
            })
    else:
        return jsonify({
            "message":"Book update failed."
        })



@app.route("/books/<book_id>",methods=["get"])
def searchBook(book_id):
    books=database.viewAllBook()
    if books is None:
        return jsonify({
            "error":"Book could not be retreieve."
        })
    for book in books:
        if book[0]==int(book_id):
            return jsonify({
                
                "message":"Book found",
                "book":book
            })
    return jsonify({
        "error":"Book not found"
    })

@app.route("/books/<book_id>",methods=["delete"])
def deleteBook(book_id):
    books=database.viewAllBook()
    if books is None:
        return jsonify({
            "error":"Book could not be retrieve."
        })
    result=False
    for book in books:
        if book[0]==int(book_id):
            result=database.deleteBook(int(book_id))
            break
    if result:
        return jsonify({
            "message":"Book deleted successfully."
            })
    return jsonify({
        "error":"Book could not be deleted."
    })

@app.route("/books/available",methods=["get"])
def availBooks():
    books=database.checkAvailableCopies()
    return jsonify(books)
    

#member

@app.route("/members",methods=["post"])
def addMember():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data required"
        })
    required_field={
        "name":str,
        "email":str,
        "phone":str,
        "address":str
    }
    for key,value in data.items():
        if key not in required_field:
            return jsonify({
                "error":f"{key} is not allow."
            })
    for key,value in required_field.items():
        if key not in data:
            return jsonify({
                "error":f"{key} is required."
            })
        else:
            if not isinstance(data[key],value):
                return jsonify({
                    "error":f"{key} must be {value.__name__}."
                })
           
    member=Member(data["name"],data["email"],data["phone"],data["address"])
    result=False
    result=database.registerMember(member)
    if result:
        return jsonify({
            "message":"Member added successfully."
        })
    else:
        return jsonify({
            "message":"Member not added."
        })
        

@app.route("/members",methods=["get"])
def viewMember():
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        })
    return jsonify(members)

@app.route("/members/member_id/<member_id>",methods=["get"])
def searchMemberByID(member_id):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        })
    for member in members:
        if member[0]==int(member_id):
            return jsonify({
                "message":"Member found.",
                "member":member
            })
    return jsonify({
        "error":"Member not fould."
    })

@app.route("/members/name/<name>",methods=["get"])
def searchMemberByName(name):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        })
    for member in members:
        if member[1]==name:
            return jsonify({
                "message":"Member found.",
                "member":member
            })
    return jsonify({
        "error":"Member not fould."
    })
    

@app.route("/members/email/<email>",methods=["get"])
def searchMemberByEmail(email):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        })
    for member in members:
        if member[2]==email:
            return jsonify({
                "message":"Member found.",
                "member":member
            })
    return jsonify({
        "error":"Member not fould."
    })

@app.route("/members/<member_id>",methods=["patch"])
def updateMember(member_id):
    members=database.viewAllMember()
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data are required."
        })
    if not isinstance(data,dict):
        return jsonify({
            "error":"json data must be an object."
        })
    if not data:
        return jsonify({
            "error":"Atleast one field is required."
        })
    if members is None:
        return jsonify({
            "error":"Member could not be retrieved."
        })
    required_field={
        "name":(str,1),
        "email":(str,2),
        "phone":(str,3),
        "address":(str,4)
    }
    for key,value in data.items():
        if key not in required_field:
            return jsonify({
                "error":f"{key} is not allow."
            })
        if not isinstance(value,required_field[key][0]):
            return jsonify({
                "error":f"{key} must be {required_field[key][0].__name__}"
            })
        

    found=False
    for member in members:
        if member[0]==int(member_id):
            found=True
            member=list(member)
            for key,value in data.items():
                member[required_field[key][1]]=value
            break
    if not found:
        return jsonify({
            "error":"Member not found."
        })

    member=Member(member[1],member[2],member[3],member[4],member[0],member[5])
    result=False
    result=database.updateMember(member)
    if result:
        return jsonify({
            "message":"Update member successfully."
        })
    else:
        return jsonify({
            "message":"Update failed."
        })


    

@app.route("/members/<member_id>",methods=["delete"])
def deleteMember(member_id):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Members could not be retrieved."
        })
    result=False
    for member in members:
        if member[0]==int(member_id):
            result=database.deleteMember(int(member_id))
            break
    if result:
        return jsonify({
            "message":"Member deleted successfully."
        })
    else:
        return jsonify({
            "message":"Member not deleted."
        })


#borrow
@app.route("/borrows",methods=["post"])
def borrowsBook():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data is required."
        })
    if not isinstance(data,dict):
        return jsonify({
            "error":"Json must be an object."
        })
    required_field={
        "book_id":(int,1),
        "member_id":(int,2)
    }
    for field in data:
        if field not in required_field:
            return jsonify({
                "error":f"{field} is not allow."
            })
    for field in required_field:
        if field not in data:
            return jsonify({
                "error":f"{field} is required."
            })
    for key,value in required_field.items():
        if not isinstance(data[key],value[0]):
            return jsonify({
                "error":f"{key} must be {value[0].__name__}"
            })
    result=False
    borrow=Borrow(data["book_id"],data["member_id"])
    result=database.borrowBook(borrow)
    if result:
        return jsonify({
            "message":"Borrowed successfully."
        })
    else:
        return jsonify({
            "message":"Borrowed failed."
        })   

@app.route("/borrows/<borrowing_id>",methods=["patch"]) 
def returnBooks(borrowing_id):

    result=database.returnBook(borrowing_id)
    if result:
        return jsonify({
            "message":"Return successfully."
        })
    else:
        return jsonify({
            "message":"Return Failed."
        })

@app.route("/borrows/history",methods=["get"])
def borrowsHistory():
    History=database.borrowHistory()
    return jsonify(History)

@app.route("/borrows/current/borrow",methods=["get"])
def currentBorrows():
    History=database.currentBorrow()
    return jsonify(History)

@app.route("/borrows/current/overdue",methods=["get"])
def currentOverdues():
    Due=database.currentOverdue()
    return jsonify(Due)

@app.route("/borrows/overdue/history",methods=["get"])
def overDuesHistory():
    overdue=database.overdueHistory()
    return jsonify(overdue)



#category

@app.route("/categories",methods=["get"])
def viewAllCategories():
    categories=database.viewAllCategory()
    return jsonify(categories)




if "__main__"==__name__:
    app.run()
