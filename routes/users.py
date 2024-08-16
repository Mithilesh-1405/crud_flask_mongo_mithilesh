from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from marshmallow import ValidationError
from flask import Blueprint
from utils.inputValidators import user_schema
from bson.objectid import ObjectId

users_bp= Blueprint('users', __name__)

@users_bp.route('/')
def landingPage():
    return "Welcome to Flask Application for CRUD operations on MongoDB"

# Get All users
@users_bp.route('/users', methods=['GET'])
def getAllUsers():
    from app import mongo
    
    allUsers = mongo.db.users.find({})
    if not allUsers:
        return jsonify({
            "message":"No users found!"
        }),404
    else:
        users=[]
        for user in allUsers:
            currentUser={
                "id":str(user["_id"]),
                "username":user.get("name"),
                "email":user.get("email")
            }
            users.append(currentUser)
        
        return jsonify({
            "users":users
        }),200
    
# Get a specific user
@users_bp.route('/users/<id>', methods=['GET'])
def getSpecificUser(id):
    from app import mongo
    dbQuery = {"_id":ObjectId(id)}
    user = mongo.db.users.find_one(dbQuery)
    if not user:
        return jsonify({
            "Error Message":"User not found",
        }),404
    else:
        return jsonify({
            "id":id,
            "name":user['name'],
            "email":user['email']       
        }),200

# Add a user
@users_bp.route('/users', methods=['POST'])
def addUsers():
    from app import mongo
    data = request.get_json()
    try:
        user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    
    #check if username or email is already taken
    if(name and email and password):
        checkName = mongo.db.users.find_one({"name":name})
        if not checkName:
            checkEmail = mongo.db.users.find_one({"email":email})
            if not checkEmail:
                hashed_password = generate_password_hash(password)
                result = mongo.db.users.insert_one({'name': name, 'email': email, 'password': hashed_password})

                if not result.inserted_id:
                    return jsonify({"message":"User could not be inserted"}), 500
                
                return jsonify({
                    "message":"Successfully inserted a user",
                    "id":str(result.inserted_id),
                }),200
            else:
                return jsonify({
                    "message":"Email is already taken, please choose another email or try logging in",
                })
        else:
            
            return jsonify({
                "message":"Username is already taken, please choose another username",
            } )
    else:
        return jsonify({
            "Error Message":"The data is not complete, please fill all the fields",
        }),400
        
# Delete a user
@users_bp.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    from app import mongo
    deleteStatus = mongo.db.users.delete_one({"_id":ObjectId(id)})
    if not deleteStatus.deleted_count:
        return jsonify({
            "Error Message":"User not found",
        }),500
    
    else:
        return jsonify({
            "message":"User Deleted succesfully",
            "id":id
        }),200

# Update a user
@users_bp.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    from app import mongo
    data = request.get_json()
    
    try:
        user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    
    if(name and email and password):
        hashedPassword = generate_password_hash(password)
        user = mongo.db.users.update_one({"_id":ObjectId(id)},{"$set":{'name': name, 'email': email, 'password': hashedPassword}})
        if not user.matched_count:
            return jsonify({
                "Error Message":"User Update failed, User not found",
            }),404
        elif not user.modified_count:
            return jsonify({
                "message":"User not modified, no changes were applied",    
            }),200
        else:
            return jsonify({
                "message":"User Updated succesfully",
                "id":id
            }),200
    else:
        return jsonify({
            "message":"The data is not complete, please fill all the fields"
        }),400

