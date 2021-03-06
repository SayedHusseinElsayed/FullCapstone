import os
from flask import (
  Flask,
  request,
  jsonify,
  abort
)
from flask_migrate import Migrate
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import *
from auth import *


def create_app(test_config=None):
 app = Flask(__name__)
 setup_db(app)
 migrate = Migrate(app , db)
 CORS(app)
 with app.app_context():
       db.create_all()

 @app.route('/')
 def testapp():
    return 'Hello, Sayed Hussein, the app is working'

 @app.after_request
 def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

 @app.route('/headers')
 #@requires_auth('get:drinks-detail')
 def hello(jwt):
    print(jwt)
    return 'Hello, Sayed Hussein, the app is working'


 @app.route('/drinks', methods=['GET'])
 def get_drinks():
    drinks_all = Drink.query.all()
    drinks = [drink.short() for drink in drinks_all]
    if len(drinks) == 0:
        abort(404)

    return jsonify({
      'success': True ,
      'drinks' : drinks 
    })


 @app.route('/drinks-detail', methods=['GET'])
 @requires_auth('get:drinks-detail')
 def get_drinks_details(self):
    drinks_all = Drink.query.all()
    print("it works here ")
    print(drinks_all)
    drinks = [drink.long() for drink in drinks_all]
    if len(drinks) == 0:
        abort(404)

    return jsonify({
      'success': True ,
      'drinks' : drinks 
    })



 @app.route('/drinks', methods=['post'])
 @requires_auth('post:drinks')
 def create_new_drink(self):
    body = request.get_json()
    new_title= body.get('title')
    new_recipe= body.get('recipe')
    new_category_id= body.get('category_id')
   
    
    new_drink = Drink(title=new_title ,category_id=new_category_id, recipe=json.dumps(new_recipe))
    new_drink.insert()
    drinks_all = Drink.query.all()
    drinks = [drink.long() for drink in drinks_all]

    return jsonify ({
        "success": True ,
        "drinks": drinks,     
      })


 @app.route('/drinks/<int:id>', methods=['PATCH'])
 @requires_auth('patch:drinks')
 def update_drink(jwt,id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    body = request.get_json()
    drink.title = body.get('title', drink.title)
    drink.recipe = json.dumps(body.get('recipe'))
    drink.update()
    drinks_all = Drink.query.all()
    drinks = [drink.long() for drink in drinks_all]

    return jsonify ({
        "success": True ,
        "drinks": drinks, 
        "modiefed_drink_id" : id
      })


 @app.route('/drinks/<int:id>', methods=['DELETE'])
 @requires_auth('delete:drinks')
 def delete_specific_drink(jwt,id) :
    selected_drink=Drink.query.get(id)
    selected_drink.delete()
    drinks = Drink.query.all()
    

    if selected_drink is None:
      abort(404)
    
    
    return jsonify ({
        'success': True ,
        'deleted' : id 
      })
    
 #Endpoints for Category class
 #Get all categories
 @app.route('/categories', methods=['GET'])
 def get_categories():
    categories_all = Category.query.all()
    categories = [category.long() for category in categories_all]

    if len(categories) == 0:
        abort(404)

    return jsonify({
      'success': True ,
      'categories' : categories
    })

 #Delete category
 @app.route('/categories/<int:category_id>', methods=['DELETE'])
 @requires_auth('delete: categories')
 def delete_category(jwt,category_id):
    category = Category.query.filter(Category.id==category_id).one_or_none()
    
    if category is None:
      abort(404)

    category.delete()

    return jsonify({
      'success': True
    })  
  
#Post category
 @app.route('/categories', methods=['POST'])
 @requires_auth('post:categories')
 def add_category(self):
  
    try:
      data = {
        'name': request.get_json()['name']
      }

      category = Category(**data)
      category.insert()
  
      result = {
        'success': True,
      }
      return jsonify(result)

    except:

     return abort(422)




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

 @app.errorhandler(404)
 def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404


 @app.errorhandler(400)
 def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Permission is not included in the JWT"
                    }), 400

 @app.errorhandler(401)
 def unauthorized (error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

 @app.errorhandler(405)
 def invalid_method (error):
    return jsonify({
                    "success": False, 
                    "error": 405,
                    "message": "invalid_method"
                    }), 405

  
 @app.errorhandler(403)
 def forbidden (error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": "forbidden"
                    }), 403
 
 @app.errorhandler(500)
 def server_error (error):
    return jsonify({
                    "success": False, 
                    "error": 500,
                    "message": "server_error"
                    }), 500
              
 @app.errorhandler(409)
 def duplicate_resource (error):
    return jsonify({
                    "success": False, 
                    "error": 409,
                    "message": "duplicate_resource"
                    }), 409





 return app 

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
