"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token  
from flask_jwt_extended import get_jwt_identity 
from flask_jwt_extended import jwt_required  
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, CollabUser, Collaboration, AttributeDescription, Observation, Mushrooms, Commentary, Post
#from models import Person

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWTSECRETKEY"] = os.environ.get('JWT_SECRET')
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
CORS(app)
db.init_app(app)
setup_admin(app)

# Handle/serialize errors like a JSON object



@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


""" @app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
 """


@app.route('/api/v1/auth/register', methods=['GET', 'POST'])
#@jwt_required()
def register_user():
    #current_user = get_jwt_identity()
    if request.method == 'POST':
        response_body_User = request.get_json()
        print(response_body_User)

        if response_body_User is None:
            raise APIException(
                "You need to specify the request body as a json object", status_code=400)
        if 'first_name' not in response_body_User:
            raise APIException(
                'You need to specify your first_name', status_code=400)
        if 'last_name' not in response_body_User:
            raise APIException(
                'You need to specify your last_name', status_code=400)
        if 'email' not in response_body_User:
            raise APIException(
                'You need to specify an email', status_code=400)
        if 'password' not in response_body_User:
            raise APIException(
                'You need to specify a password', status_code=400)

        register_user =  User.query.all()      
        print(register_user)  
        new_user = User(first_name=response_body_User['first_name'],
                        last_name=response_body_User['last_name'],
                        email=response_body_User['email'],
                        password=bcrypt.generate_password_hash(response_body_User['password']).decode())
        db.session.add(new_user)
        db.session.commit()
        serialized_register_user = map(lambda user: user.serialize, register_user)
        print(serialized_register_user)
        filtered_users = list(filter(lambda user: user['first_name'] == response_body_User['first_name'], serialized_register_user))
        return {"User": list(filtered_users), "Everything in it's Right Place": 200}
    elif request.method == 'GET':
        register_user =  User.query.all()
        serialized_register_user = map(lambda user: user.serialize(), register_user)
        return {'User': list(serialized_register_user), 'status': 200}




@app.route("/api/v1/auth/user", methods=['GET'])
@jwt_required()
def regular_user():
    current_user = get_jwt_identity()
    print(current_user)
    if request.method == 'GET':
        users = User.query.all()
        serialized_users = map(lambda user: user.serialize, regular_user)
        return {"users": list(serialized_users),"status" : 200}
    elif request.method == 'POST':
        return'Hola POST'
    else:
        abort(405)    
   
#    if email != "test" or password != "test":
#        return jsonify({"msg": "Bad username or password"}), 401

#    access_token = create_access_token(identity=User.id)
#    return jsonify({"token" : access_token, "user_id":User.id})








# @app.route("/api/v1/auth/token", methods=["POST"])
# def create_token():
#     email = request.json.get("email", None)
#     password = request.json.get("password", None)
#     if email != "test" or password != "test":
#         return jsonify({"msg": "Bad username or password"}), 401

#     access_token = create_access_token(identity=email)
#     return jsonify(access_token=access_token)





@app.route('/api/v1/auth/login', methods=['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        response_login = request.get_json()
        print(response_login)
        if response_login is None:
            raise APIException(
                "You need to specify the request body as a json object", status_code=400)
        if 'email' not in response_login:
            raise APIException(
                'You need to specify an email', status_code=400)
        if 'password' not in response_login:
            raise APIException(
                'You need to specify a password', status_code=400)

        login_user =  User.query.all()        
        print(login_user)        
        serialized_login_user = map(lambda user: user.serialize, login_user)
        filtered_login = list(filter(lambda user: user['email']  == response_login['email'], serialized_login_user ))
        if(filtered_login.count == 0):
            return{"status": 400, "message": "usuario o contraseña incorrectos"}
        elif(bcrypt.check_password_hash(filtered_login[0]['password'], response_login['password'])): 
            login_token = create_access_token(identity=filtered_login[0]['first_name'])
            return {"User": list(filtered_login), "token": login_token, "Everything in it's Right Place": 200}
        else:
            return abort(401)
    elif request.method == 'GET':
        login_user =  User.query.all()
        serialized_login_user = map(lambda user: user.serialize, login_user)
        return {"User": list(serialized_login_user), "status": 200}




@app.route('/register_collab', methods=['POST'])
def collab_register():

    collaboration_body = request.get_json()

    if collaboration_body is None:
        raise APIException(
            "You need to specify the Collaboration as a json object", status_code=400)
    if 'mush_img' not in collaboration_body:
        raise APIException(
            'You need to specify an image of your mushroom', status_code=400)
    if 'spore_img' not in collaboration_body:
        raise APIException(
            'You need to specify an image of the spores of your mushroom', status_code=400)
    if 'description' not in collaboration_body:
        raise APIException(
            'You need to specify the description of your collaboration', status_code=400)
    if 'species' not in collaboration_body:
        raise APIException(
            'You need to specify the specie name of the mushroom', status_code=400)
    if 'location' not in collaboration_body:
        raise APIException(
            'You need to specify the location of you found this mushroom', status_code=400)
    if 'substrate' not in collaboration_body:
        raise APIException(
            'You need to specify the substrate of this mushroom', status_code=400)
    if 'gills' not in collaboration_body:
        raise APIException(
            'You need to specify if the mushroom have gills or not', status_code=400)
    if 'pores' not in collaboration_body:
        raise APIException(
            'You need to specify if the mushroom have pores or not', status_code=400)
    if 'pileus_diameter' not in collaboration_body:
        raise APIException(
            'You need to specify the pileus diameter', status_code=400)
    if 'shape' not in collaboration_body:
        raise APIException(
            'You need to specify the shape of the mushroom', status_code=400)
    if 'pileus_color' not in collaboration_body:
        raise APIException(
            'You need to specify the pileus color', status_code=400)
    if 'margin' not in collaboration_body:
        raise APIException(
            'You need to specify the margin of the mushroom', status_code=400)
    if 'height' not in collaboration_body:
        raise APIException(
            'You need to specify the height of the mushroom', status_code=400)
    if 'foot_color' not in collaboration_body:
        raise APIException(
            'You need to specify the foot color', status_code=400)
    if 'ring' not in collaboration_body:
        raise APIException(
            'You need to specify a description of the rings', status_code=400)
    if 'foot_diameter' not in collaboration_body:
        raise APIException(
            'You need to specify the foot diameter', status_code=400)
    if 'volva' not in collaboration_body:
        raise APIException(
            'You need to specify a description of the volva', status_code=400)

    new_collaboration = (Collaboration(mush_img=collaboration_body['mush_img'], spore_img=collaboration_body['spore_img'],description=collaboration_body['description']).AttributeDescription(species=collaboration_body['species'], location=collaboration_body['location'], substrate=collaboration_body['substrate'], gills=collaboration_body['gills'], pores=collaboration_body['pores'], pileus_diameter=collaboration_body['pileus_diameter'], shape=collaboration_body['shape'], pileus_color=collaboration_body['pileus_color'], margin=collaboration_body['margin'], height=collaboration_body['height'], foot_color=collaboration_body['foot_color'], ring=collaboration_body['ring'], foot_diameter=collaboration_body['foot_diameter'], volva=collaboration_body['volva']))
    db.session.add(new_collaboration)
    db.session.commit()
    return "Everything in it's Right Place", 200


@app.route('/observation', methods=['POST'])

def observation_register():

    observation_body = request.get_json()

    if observation_body is None:
        raise APIException(
            "You need to specify the request body as a json object", status_code=400)
    if 'title' not in observation_body:
        raise APIException(
            'You need to specify a title for your observation', status_code=400)
    if 'body' not in observation_body:
        raise APIException(
            'You need to specify your observation', status_code=400)
    if 'img_url' not in observation_body:
        raise APIException('You need to upload an image of your observation', status_code=400)

    new_observation = Observation(title=observation_body['title'],
                 body=observation_body['body'],
                 img_url=observation_body['img_url'])
    db.session.add(new_observation)
    db.session.commit()

    return "Everything in it's Right Place", 200



@app.route('/mushroom', methods=['POST']) #minusculas para las rutas
def mushroom_register():  #minuscula solo las clases van con mayusculas
    observation_mushroom = request.get_json()

    if observation_mushroom is None:
        raise APIException(
            "You need to specify the request body as a json object", status_code=400)
    if 'local_name' not in observation_mushroom:
        raise APIException(
            'You need to specify a local name for your mushroom', status_code=400)
    if 'scientific_name' not in observation_mushroom:
        raise APIException(
            'You need to specify a scientific name of the mushroom', status_code=400)
    if 'edible' not in observation_mushroom:
        raise APIException('You need to specify if this mushroom can be eaten', status_code=400)
    if 'hallucinogen' not in observation_mushroom:
        raise APIException('You need to specify if this mushroom can be hallucinogen', status_code=400)
    if 'location' not in observation_mushroom:
        raise APIException('You need to specify the location where you find this mushroom', status_code=400)
    if 'data_description' not in observation_mushroom:
        raise APIException('You need to specify a description where you find this mushroom', status_code=400)
    if 'recipe' not in observation_mushroom:
        raise APIException('You need to specify a recipe for this this mushroom', status_code=400)
    
    new_mushroom = Mushrooms(local_name=observation_mushroom['local_name'],
                 scientific_name=observation_mushroom['scientific_name'],
                 edible=observation_mushroom['edible'],
                 hallucinogen=observation_mushroom['hallucinogen'],
                 location=observation_mushroom['location'],
                 data_description=observation_mushroom['data_description'],
                 recipe=observation_mushroom['recipe'])
    db.session.add(new_mushroom)
    db.session.commit()

    return "Everything in it's Right Place", 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
