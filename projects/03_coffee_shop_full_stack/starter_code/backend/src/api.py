import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

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
db_drop_and_create_all()

## ROUTES

'''
Loging route for Auth0
'''
@app.route('/loggedin',methods=['GET'])
def loggedin():
    return jsonify({
        'message':'logged in'
    })
'''

@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@route('/drinks', methods = ['GET'])
def get_drinks():

    try:
        drinks = Drink.query.all()
    except:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in drinks]
        }) , 200
        


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def retreive_drink_detail(token):
    try:
        drinks = Drink.query.all()
    except:
        abort(404)
    
    else:
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in drinks]
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def post_new_drink(token):
    request_json = request.get_json()

    if 'recipe' and 'title' not in request:
        abort(422)
    
    
    try:
        newDrink = Drink()
        newDrink.title = request_json['title']
        newDrink.recipe = json.dumps(request_json['recipe'])
        newDrink.insert()

    except:
        abort(400)
    else:
        return jsonify({
            'success': True,
            'drinks': [newDrink.long()] 
        })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def update_existing_drink(id):

        request_json = request.get_json()
        retreived_drink = Drink.query.filter(Drink.id==id).first_or_404()

        try:
            if 'title' and 'recipe' not in request_json:
                abort(404)

            retreived_drink.title = request_json['title']
            retreived_drink.recipe = json.dumps(request_json['recipe'])
            retreived_drink.update()
        except:
            abort(400)
        else:
            jsonify({
                'success': True,
                'drinks': [retreived_drink.long()]
            })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_existing_drink(token,id):

    retreived_drink = Drink.query.filter(Drink.id == id).first_or_404()
    retreived_drink.delete()

    return jsonify({
        'success':True,
        'delete':retreived_drink.id
    })

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
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'mesage': 'resource not found'
    }),404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''

@app.errorhandler(AuthError)
def auth_error_handle(error):
   
   
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }),error.status_code

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400
