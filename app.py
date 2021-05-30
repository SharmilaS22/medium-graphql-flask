from flask import Flask
import graphene
app = Flask(__name__)

from graphene import ObjectType, Schema, Argument, String, Int,  Field, NonNull, List
 

'''
    Simple query to return string
'''
class Query(ObjectType):

    hello = String( 
        name = Argument(String, default_value = "World"), 
        age = Argument(Int, default_value = 20),
        description = 'Hello world query'
    )    
    # resolve function
    def resolve_hello(self, info, name, age):
        return 'Hello ' + name + ' of age ' + str(age)

my_query = """
    {
        hello ( name = "Sharmi" )
    }
"""



class Book(ObjectType):
    id     = NonNull(Int)
    title  = String()
    author = String()

# database
book_array = [
    Book(id = 1, title = "Angels and Demons", author = "Dan Brown"),
    Book(id = 2, title = "And Then There Were None", author = "Agatha Christie"),
    Book(id = 3, title = "The Lightning Thief", author = "Rick Riordon")
]
# print(book_array)


'''
    Query to return an object
'''

class BookQuery (ObjectType):

    book = Field(Book)

    def resolve_book(self, info):

        new_book = book_array[0]

        return new_book

book_query = """
    {
        book {
            id, title
        }
    }
"""


'''
    takes arguments - returns object
'''

class BookArgsQuery (ObjectType):

    book_details = Field(Book, id = Argument(Int))
    # this is called from query as 'bookDetails' (camelcase)

    def resolve_book_details(self, info, id):

        # return the book which matches the id given
        for book_obj in book_array:
            if ( book_obj.id == id ):
                new_book = book_obj

        return new_book

book_with_args_query = """
    {
        bookDetails (id: 3 ) {
            id, title
        }
    }
"""

'''
    returns all books
'''

class BooksQuery (ObjectType):

    book_details = Field(Book, id = Argument(Int))

    books = List(Book)

    def resolve_book_details(self, info, id):

        # return the book which matches the id given
        for book_obj in book_array:
            if ( book_obj.id == id ):
                new_book = book_obj

        return new_book

    def resolve_books(self, info):
        return book_array

books_query = """
    {
        books {
            id, title
        }
    }
"""

    
'''
    Schema, and executing query
'''
QueryForSchema = BooksQuery
QueryToExecute = books_query

schema = Schema(query=QueryForSchema)

result = schema.execute(QueryToExecute)
print(result)


@app.route('/')
def root_route():
    return {
        "data": result.data
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)