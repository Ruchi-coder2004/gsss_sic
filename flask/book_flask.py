from flask import Flask, jsonify, request
from book_db_operation import BookOperations as bookOprs, Book

book_obj = bookOprs()
book_obj.create_database()
book_obj.create_table()

app = Flask(__name__)

@app.route('/book',methods=['POST'])
def book_obj_create():
    body = request.get_json()
    new_book = Book(body['title'], body['author'], body['price'], body['publisher'], body['edition'], body['number_of_pages'])
    print(new_book)
    id = book_obj.create_row(new_book)
    book = book_obj.search_row(id)
    book_dict = {'id':book[0], 'title':book[1], 'author':book[2], 'price':book[3], 'publisher': book[4], 'edition': book[5], 'number_of_pages': book[6]}
    return jsonify(book_dict)

@app.route('/book/<id>',methods=['GET'])
def book_obj_read_by_id(id):
    book = book_obj.search_row(id)
    if book == None:
        return jsonify("book not found")
    book_dict = {'id':book[0], 'title':book[1], 'author':book[2], 'price':book[3], 'publisher':book[4], 'edition':book[5], 'number_of_pages':book[6]}
    return jsonify(book_dict)

@app.route('/book',methods=['GET'])
def book_obj_read_all():
    book_obj_list = book_obj.list_all_rows()
    book_obj_dict = []
    for book in book_obj_list:
        book_obj_dict.append({'id':book[0], 'title':book[1], 'author':book[2], 'price':book[3], 'publisher':book[4], 'edition':book[5], 'number_of_pages':book[6]})
    return jsonify(book_obj_dict)

@app.route('/book/<id>',methods=['PUT'])
def book_obj_update(id):
    body = request.get_json()
    old_book_obj = book_obj.search_row(id)
    if not old_book_obj:
        return jsonify({'message': 'book not found'})
    old_book_obj = []
    old_book_obj.append(body['title'])
    old_book_obj.append(body['author'])
    old_book_obj.append(body['price'])
    old_book_obj.append(body['publisher'])
    old_book_obj.append(body['edition'])
    old_book_obj.append(body['number_of_pages'])
    old_book_obj.append(id)
    old_book_obj = tuple(old_book_obj)
    book_obj.update_row(old_book_obj)

    book = book_obj.search_row(id)
    person_dict = {'id':book[0], 'title':book[1], 'author':book[2], 'price':book[3], 'publisher':book[4], 'edition':book[5], 'number_of_pages':book[6]}
    return jsonify(person_dict)

@app.route('/book/<id>',methods=['DELETE'])
def book_obj_delete(id):
    old_book_obj = book_obj.search_row(id)
    if not old_book_obj:
        return jsonify({'message': 'book not found', 'is_error': 1})
    book_obj.delete_row(id)
    return jsonify({'message': 'book is deleted', 'is_error': 0})

app.run(debug=True)