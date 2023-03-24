
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, User_info, Foto, Direccion, Categorias, Peques, Mayores, Mascota, Resenas, Valoracion
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required



api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
# hacemos una consulta a la tabla para saber si el user existe
    user = Users.query.filter_by(email=email).first()
# si no existe devuelvo msg
    if user is None:
        return jsonify({"msg": "User dosn´t exist"}), 404
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


# endpoint profile
@api.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    # Accede a la identidad del usuario actual con get_jwt_identity

    current_user = get_jwt_identity()
    user = Users.query.filter_by(email=current_user).first()

    return jsonify({"result": user.serialize()}), 200


@api.route("/validtoken", methods=["GET"])
@jwt_required()
def valid_token():
    # Access the identity of the current user with get_jwt_identity

    current_user = get_jwt_identity()

    user = Users.query.filter_by(email=current_user).first()
    if user != None:

        return jsonify({"isLogged": True}), 200
    else:
        return jsonify({"isLogged": False}), 401


# creacion de users
@api.route('/user', methods=['POST'])
def create_user():
    request_body = request.json
    message = "ya existe el usuario"
    status = 400
    user_query = Users.query.filter_by(email=request_body["email"]).first()

    if user_query is None:
        user = User(email=request_body["email"],
                    password=request_body["password"],
                    nombre=request_body["nombre"],
                    apellido=request_body["apellido"],)

        db.session.add(user)
        db.session.commit()
        message = "el usuario se a creado con exito"
        status = 200

    response_body = {
        "msg": message

    }

    return jsonify(response_body), status

@api.route('/user_info', methods=['POST'])
@jwt_required()
def create_user_info():
    request_body = request.json
    current_user = get_jwt_identity()

    user = Users.query.filter_by(email=current_user).first()
    if user != None:
        user_info = User_info(descripcion=request_body["descripcion"],
                            experiencia=request_body["experiencia"],
                            tarifa=request_body["tarifa"],
                            plus_tarifa=request_body["plus_tarifa"],
                            puntuacion_global=request_body["puntuacion_global"],
                            cantidad_votos=request_body["cantidad_votos"],
                            numero_telefono=request_body["numero_telefono"],
                            fecha_nacimiento=request_body["fecha_nacimiento"],
                            genero=request_body["genero"],
                            educacion=request_body["educacion"],
                            redes_sociales=request_body["redes_sociales"],
                            tipo_servicios=request_body["tipo_servicios"])
        user.user_info.append(user_info)
        db.session.add(user)
        db.session.commit()

        response_body = {
            "msg": "ok",
            "user":user.serialize(),
            "user_info":user_info.serialize(),
        }
        return jsonify(response_body), 200

@api.route('/tipoUsuario', methods=['PUT'])
@jwt_required()
def set_es_cuidador():
    request_body = request.json
    current_user = get_jwt_identity()

    user = Users.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({"msg":"No se ha encontrado el usuario"}), 404
    if request_body['categoria'] == "familia":
        user.es_cuidador = False
    elif request_body['categoria'] == "cuidador":
        user.es_cuidador = True
    else:
        return jsonify({"msg":"El body no coincide"}),400
    
    db.session.commit()

    return jsonify({"msg": "Se ha actualizado el tipo de usuario"}), 200


@api.route('/informacion/<int:user_id>', methods=['GET'])
def set_info_user(user_id):
    user_query = Users.query.filter_by(id=user_id).first()
    if user_query != None and user_query.is_active is True:
        user_info_2 = Users.query.filter_by(id=user.id).first()

        print(user_info_2.serialize2())
        response_body = {
            "msg": "ok",
            "results": user_info_2.serialize2()
        }    
        return jsonify(response_body), 200
    else : 
        return jsonify({"msg":"No se ha encontrado"}), 404
    return jsonify({"msg":"No se ha encontrado"}), 404




@api.route('/user_info/<int:user_id>', methods=['GET'])
def set_info_user(user_id):
    user_query = Users.query.filter_by(id=user_id).first()
    if user_query != None and user_query.is_active is True:
        info = user_query.user_info[-1]
        
        response_body = {
            "msg": "ok",
            "results": {"info" : info.serialize(),
                        "datospersonales": user_query.serialize()
                        }
        }    
        return jsonify(response_body), 200
    else : 
        return jsonify({"msg":"No se ha encontrado"}), 400
        
# obtiene los datos de un usuario
@api.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user_query = Users.query.filter_by(id=user_id).first()
    print(user_query)
#querys o consultas
    response_body = {
        "msg": "ok",
        "result": user_query.serialize()
    }
    return jsonify(response_body), 200    
