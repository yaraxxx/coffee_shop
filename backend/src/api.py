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
    drinks = Drink.query.all()
    print('test')
    if drinks is None:
        abort(404)
    drinks_list = []
    for drink in drinks:
        drinks_list.append(drink.long())
    return jsonify({"success":True , "drinks":drinks_list})







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
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()

        drinks_list = []
        for drink in drinks:
            drinks_list.append(drink.long())
        return jsonify({"success": True , "drinks": drinks_list})
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
def add_drink(payload):
    try:
        body = request.get_json()
        if(body is None):
            abort(404)
        new_drink = Drink(
                title = body.get('title'),
                recipe =json.dumps(body.get('recipe'))
                )
        new_drink.insert()
        drink = Drink.query.filter_by(id=new_drink.id).first()
        return jsonify({"success": True , "drinks": [drink.long()]})
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
def update_drink(payload,id):
    try:
        drink = Drink.query.filter_by(id = id).one_or_none()
        if drink is None:
            abort(404)
            print(sys.exc_info())

        body = request.get_json()
        title_update = body.get('title')
        recipe_update = json.dumps(body.get('recipe'))
        if title_update:
            drink.title = title_update
        if recipe_update:
            drink.recipe = recipe_update

        drink.update()

        updated_drink = drink.long()
        return jsonify({"success": True , "drinks": updated_drink})
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
def delete_drink(payload,id):
    try:
        drink = Drink.query.filter_by(id = id).one_or_none()
        if drink is None:
            abort(404)
            print(sys.exc_info())

        drink.delete()
        return jsonify({"success": True , "delete": id})
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
@app.errorhandler(AuthError)
def AuthError(error):
    # response = jsonify(ex.error)
    # response.status_code = ex.status_code
    # return response
    return jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error
                    }), 401
