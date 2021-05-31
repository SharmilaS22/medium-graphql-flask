from flask import Flask
app = Flask(__name__)

from graphene import ObjectType, Schema, Argument, String, Int,  Field, NonNull, List
 

@app.route('/')
def root_route():
    return 'Hello World!'


'''
    Simple query to return string -  Query and Schema
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

helloSchema = Schema(query = Query)


#    Get a String 
#    helloSchema
#   
#   http://localhost:5000/hello/Percy

@app.route('/hello/<name>')
def hello_world(name):
    # query
    my_query = """
        {
            hello ( name : "%s" )
        }
    """%(name)

    result = helloSchema.execute(my_query)

    return {
        "data": result.data['hello']
    }



# Book object
class Book(ObjectType):
    id     = NonNull(Int)
    title  = String()
    author = String()

# array of objects
book_array = [
    Book(id = 1, title = "Angels and Demons", author = "Dan Brown"),
    Book(id = 2, title = "And Then There Were None", author = "Agatha Christie"),
    Book(id = 3, title = "The Lightning Thief", author = "Rick Riordon")
]
# print(book_array)


''' ------------------------------------------------------------------------
    Query to return an object --  Query and Schema
'''
class BookQuery (ObjectType):

    book = Field(Book)

    def resolve_book(self, info):

        new_book = Book( id = 1, title = "Six of Crows", author = "Leigh Bardugo" )

        return new_book

bookSchema = Schema(query=BookQuery)


#   Get a Book object
#   bookSchema
# 
#   http://localhost:5000/book

@app.route('/book')
def get_book():

    book_query = """
        {
            book {
                id, title
            }
        }
    """

    result = bookSchema.execute(book_query)

    return {
        "data": result.data['book']
    }



''' -------------------------------------------------------
    takes arguments - returns object -  Query and Schema
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

bookArgsSchema = Schema(query=BookArgsQuery)


#   Get a Book by Id
#   bookArgsSchema
# 
#   http://localhost:5000/book/2
@app.route('/book/<int:id>')
def get_book_by_id(id):
  
    book_with_args_query = """
        {
            bookDetails (id: %d ) {
                id, title
            }
        }
    """%(id)

    result = bookArgsSchema.execute(book_with_args_query)

    return {
        "data": result.data['bookDetails']
    }

''' --------------------------------------------------------------
    returns all books - Query and Schema
'''
class BooksQuery (ObjectType):

    book_details = Field(Book, id = Argument(Int))

    book_list = List(Book)

    def resolve_book_details(self, info, id):

        # return the book which matches the id given
        for book_obj in book_array:
            if ( book_obj.id == id ):
                new_book = book_obj

        return new_book

    def resolve_book_list(self, info):
        return book_array

booksSchema = Schema(query=BooksQuery)

#   Get all Books
#   booksSchema
# 
#   http://localhost:5000/books
@app.route('/books')
def get_all_books():

    books_query = """
        {
            bookList {
                title, author
            }
        }
    """

    result = booksSchema.execute(books_query)

    return {
        "data": result.data['bookList']
    }


if __name__ == '__main__':
    app.run(debug=True)