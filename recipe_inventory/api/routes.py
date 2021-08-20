from flask import Blueprint, json, request, jsonify
from recipe_inventory.helpers import token_required
from recipe_inventory.models import db, User, Recipe, recipe_schema, recipes_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return{'some_value': 52, 'another_value': 800}


#CREATE RECIPE API ENDPOINT
@api.route('/recipes', methods = ['POST'])
@token_required
def create_recipe(current_user_token):
    name = request.json['name']
    description = request.json['description']
    cook_time = request.json['cook_time']
    meat_or_veg = request.json['meat_or_veg']
    garnishes = request.json['garnishes']
    spices = request.json['spices']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    recipe = Recipe(name, description, cook_time, meat_or_veg, garnishes, spices, user_token = user_token)

    db.session.add(recipe)
    db.session.commit()

    response = recipe_schema.dump(recipe)
    return jsonify(response)

#Retrieve all recipes
@api.route('/recipes', methods = ['GET'])
@token_required
def get_recipes(current_user_token):
    owner = current_user_token.token
    recipes = Recipe.query.filter_by(user_token = owner).all()
    response = recipes_schema.dump(recipes)
    return jsonify(response)

#Retrieve single recipe endpoint
@api.route('/recipes/<id>', methods = ['GET'])
@token_required
def get_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    response = recipe_schema.dump(recipe)
    return jsonify(response)


#Update a recipe by ID Enpoint
@api.route('/recipes', methods = ['POST'])
@token_required
def update_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    print(recipe)
    if recipe:
        recipe.name = request.json['name']
        recipe.description = request.json['description']
        recipe.cook_time = request.json['cook_time']
        recipe.meat_or_veg = request.json['meat_or_veg']
        recipe.garnishes = request.json['garnishes']
        recipe.spices = request.json['spices']
        recipe.user_token = current_user_token.token
        db.session.commit()

        response = recipe_schema.dump(recipe)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That recipe does not exist!'})

#Delete recipe by ID
@api.route('/recipes/<id>', methods = ['DELETE'])
@token_required
def delete_recipe(current_user_token, id):
    recipe = Recipe.query.get(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()

        response = recipe_schema.dump(recipe)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That recipe does not exist!'})