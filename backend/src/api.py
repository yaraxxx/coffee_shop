import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure [DONE]
'''
@app.route('/drinks',methods=['GET'])
def view_drinks():
    try:
        drinks = Drink.query.all()

        drinks_list = []
        for drink in drinks:
            drinks_list.append(drink.short())
        return {"success":True , "drinks": drinks_list}
    except:
        abort(404)
        print(sys.exc_info())






'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure [DONE]
'''
@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    try:
        drinks = Drink.query.all()

        drinks_list = []
        for drink in drinks:
            drinks_list.append(drink.long())
        return {"success": True , "drinks": drinks_list}
    except:
        abort(404)
        print(sys.exc_info())




'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure [DONE]
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    try:
        body = request.get_json()
        new_drink = Drink(
                    title = body.get('title'),
                    recipe = body.get('recipe')
            )
        new_drink.insert()
        drink = new_drink.long()
        return {"success": True , "drinks": drink}
    except:
        abort(422)
        print(sys.exc_info())



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure [DONE]
'''
@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(id):
    try:
        drink = Drink.query.filter_by(id = id).one_or_none()
        if drink is None:
            abort(404)
            print(sys.exc_info())

        body = request.get_json()
        drink.title = body.get('title')
        drink.recipe = body.get('recipe')
        drink.update()

        updated_drink = drink.long()
        return {"success": True , "drinks": updated_drink}
    except:
        abort(422)
        print(sys.exc_info())



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure [DONE]
'''
@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    try:
        drink = Drink.query.filter_by(id = id).one_or_none()
        if drink is None:
            abort(404)
            print(sys.exc_info())

        drink.delete()
        return {"success": True , "delete": id}
    except:
        abort(422)
        print(sys.exc_info())


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "auth error"
                    }), 401
