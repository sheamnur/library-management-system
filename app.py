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
        }),500
    return jsonify(Books),200

@app.route("/books",methods=["post"])
def addBook():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data is required."
        }),400
    if not isinstance(data,dict):
        return jsonify({
            "error":"Json must be an object."
        }),400
    if not data:
        return jsonify({
            "error":"At least one field is required"
        }),400

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
            }),400
        
    for key, value in required_field.items():
        if not isinstance(data[key], value):
            return jsonify({
                "error": f"{key} must be {value.__name__}"
            }), 400


    book=Book(
        data["title"],data["author"],data["isbn"],data["category"],data["publisher"],data["publication_year"],data["total_copies"],data["available_copies"]
    )
    result=database.addBook(book)
    if result is True:
        return jsonify({
            "message":"Book add successfully."
            }),201
    elif isinstance(result,str):
        return jsonify({
            "error":result
        }),400
    return jsonify({
        "message":"Database operation failed."
    }),500

@app.route("/books/<book_id>",methods=["patch"])
def updateBook(book_id):
    books=database.viewAllBook()
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data is required."
        }),400
    if not isinstance(data,dict):
        return jsonify({
            "error":"Json must be an object."
        }),400
    if not data:
        return jsonify({
            "error":"At least one field is required"
        }),400

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
            }),400

    for key,value in required_field.items():
        if key in data:
            if not isinstance(data[key],value):
                return jsonify({
                    "error":f"{key} must be {value.__name__}"
                }),400

    

    if books is None:
        return jsonify({
            "error":"Books could not be retreived."
        }),500

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
        }),404
        

    book=Book(
        book["title"],book["author"],book["isbn"],book["category"],book["publisher"],book["publication_year"],book["total_copies"],book["available_copies"],book_id=book["book_id"]
    )
    result=False
    result=database.updateBook(book)
    if result is True:
        return jsonify({
            "message":"Book update successfully."
            }),200
    elif isinstance(result,str):
        return jsonify({
            "error":result
        })

    return jsonify({
        "message":"Book update failed."
    }),500



@app.route("/books/<book_id>",methods=["get"])
def searchBook(book_id):
    books=database.viewAllBook()
    if books is None:
        return jsonify({
            "error":"Book could not be retreieve."
        }),500
    for book in books:
        if book[0]==int(book_id):
            return jsonify({
                
                "message":"Book found",
                "book":book
            }),200
    return jsonify({
        "error":"Book not found"
    }),404

@app.route("/books/<book_id>",methods=["delete"])
def deleteBook(book_id):
    books=database.viewAllBook()
    if books is None:
        return jsonify({
            "error":"Book could not be retrieve."
        }),500
    result=False
    book_found=False
    for book in books:
        if book[0]==int(book_id):
            book_found=True
            result=database.deleteBook(int(book_id))
            break
    if not book_found:
        return jsonify({
            "error":"Book not found"
        }),404
    if result:
        return jsonify({
            "message":"Book deleted successfully."
            }),200
    return jsonify({
        "error":"Book could not be deleted."
    }),500

@app.route("/books/available", methods=["get"])
def availBooks():
    books = database.checkAvailableCopies()

    if books is None:
        return jsonify({"error": "Books could not be retrieved."}), 500

    return jsonify(books), 200

#member

@app.route("/members",methods=["post"])
def addMember():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data required"
        }),400
    if not isinstance(data,dict):
        return jsonify({
            "error":"Json must be an object."
        }),400
    if not data:
        return jsonify({
            "error":"At least one field is required"
        }),400
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
            }),400
    for key,value in required_field.items():
        if key not in data:
            return jsonify({
                "error":f"{key} is required."
            }),400
        else:
            if not isinstance(data[key],value):
                return jsonify({
                    "error":f"{key} must be {value.__name__}."
                }),400
           
    member=Member(data["name"],data["email"],data["phone"],data["address"])
    result=False
    result=database.registerMember(member)
    if result is True:
        return jsonify({
            "message":"Member added successfully."
        }),201
    elif isinstance(result,str):
        return jsonify({
            "error":result
        }),400
    return jsonify({
        "message":"Member not added."
    }),500
        

@app.route("/members",methods=["get"])
def viewMember():
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        }),500
    return jsonify(members),200

@app.route("/members/member_id/<member_id>",methods=["get"])
def searchMemberByID(member_id):
    try:
        member_id=int(member_id)
    except ValueError as e:
        return jsonify({
            "error":"Member id must be integer."
        }),400
    members=database.searchMemByID(member_id)
    if members is None:
        return jsonify({
            "error":"Memeber not found."
        }),404
    elif isinstance(members,str):
        return jsonify({
            "error":members
        }),500

    return jsonify({
        "message":"Member found.",
        "member":members
    }),200


@app.route("/members/name/<name>",methods=["get"])
def searchMemberByName(name):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        }),500
    for member in members:
        if member[1]==name:
            return jsonify({
                "message":"Member found.",
                "member":member
            }),200
    return jsonify({
        "error":"Member not fould."
    }),404
    

@app.route("/members/email/<email>",methods=["get"])
def searchMemberByEmail(email):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Memebers could not be retrieved."
        }),500
    for member in members:
        if member[2]==email:
            return jsonify({
                "message":"Member found.",
                "member":member
            }),200
    return jsonify({
        "error":"Member not fould."
    }),404

@app.route("/members/<member_id>",methods=["patch"])
def updateMember(member_id):
    members=database.viewAllMember()
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data are required."
        }),400
    if not isinstance(data,dict):
        return jsonify({
            "error":"json data must be an object."
        }),400
    if not data:
        return jsonify({
            "error":"Atleast one field is required."
        }),400
    if members is None:
        return jsonify({
            "error":"Member could not be retrieved."
        }),500
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
            }),400
        if not isinstance(value,required_field[key][0]):
            return jsonify({
                "error":f"{key} must be {required_field[key][0].__name__}"
            }),400
        

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
        }),404

    member=Member(member[1],member[2],member[3],member[4],member[0],member[5])
    result=False
    result=database.updateMember(member)
    if result:
        return jsonify({
            "message":"Update member successfully."
        }),200
    else:
        return jsonify({
            "message":"Update failed."
        }),500


    

@app.route("/members/<member_id>",methods=["delete"])
def deleteMember(member_id):
    members=database.viewAllMember()
    if members is None:
        return jsonify({
            "error":"Members could not be retrieved."
        }),500
    result=False
    found=False
    for member in members:
        if member[0]==int(member_id):
            found=True
            result=database.deleteMember(int(member_id))
            break
    if not found:
        return jsonify({
            "error":"Member not found."
        }),404
    if result:
        return jsonify({
            "message":"Member deleted successfully."
        }),200
    else:
        return jsonify({
            "message":"Member not deleted."
        }),500


#borrow
@app.route("/borrows",methods=["post"])
def borrowsBook():
    data=request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error":"Json data is required."
        }),400
    if not isinstance(data,dict):
        return jsonify({
            "error":"Json must be an object."
        }),400
    if not data:
        return jsonify({
            "error":"Atleast one field is required."
        }),400
    required_field={
        "book_id":(int,1),
        "member_id":(int,2)
    }
    for field in data:
        if field not in required_field:
            return jsonify({
                "error":f"{field} is not allow."
            }),400
    for field in required_field:
        if field not in data:
            return jsonify({
                "error":f"{field} is required."
            }),400
    for key,value in required_field.items():
        if not isinstance(data[key],value[0]):
            return jsonify({
                "error":f"{key} must be {value[0].__name__}"
            }),400
    result=False
    borrow=Borrow(data["book_id"],data["member_id"])
    result=database.borrowBook(borrow)
    if result:
        return jsonify({
            "message":"Borrowed successfully."
        }),201
    else:
        return jsonify({
            "message":"Borrowed failed."
        }),404

@app.route("/borrows/<borrowing_id>",methods=["patch"]) 
def returnBooks(borrowing_id):

    result=database.returnBook(borrowing_id)
    if result:
        return jsonify({
            "message":"Return successfully."
        }),200
    else:
        return jsonify({
            "message":"Return Failed."
        }),404

@app.route("/borrows/history",methods=["get"])
def borrowsHistory():
    History=database.borrowHistory()
    return jsonify(History),200

@app.route("/borrows/current/borrow",methods=["get"])
def currentBorrows():
    History=database.currentBorrow()
    return jsonify(History),200

@app.route("/borrows/current/overdue",methods=["get"])
def currentOverdues():
    Due=database.currentOverdue()
    return jsonify(Due),200

@app.route("/borrows/overdue/history",methods=["get"])
def overDuesHistory():
    overdue=database.overdueHistory()
    return jsonify(overdue),200



#category

@app.route("/categories",methods=["get"])
def viewAllCategories():
    categories=database.viewAllCategory()
    return jsonify(categories),200




if "__main__"==__name__:
    app.run()
