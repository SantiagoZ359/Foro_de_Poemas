from flask import request, jsonify, Blueprint
from .. import db
from main.models import PoemaModel, UsuarioModel, CalificacionModel
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

#Blueprint para acceder a los metodos de autentificacion
auth = Blueprint('auth', __name__, url_prefix='/auth')

#Metodo de logueo
@auth.route('/login', methods = ['POST'])
def login():
    #Busca al usuario en la db por email
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.email == request.get_json().get('email')).first_or_404()
    #Valida la contraseña
    if usuario.validate_pass(request.get_json().get("contraseña")):
        #Genera un nuevo token
        #Pasa el objeto usuario como identidad
        access_token = create_access_token(identity=usuario)
        #devuelve valores y el token
        data = {
            'id':str(usuario.id),
            'email':usuario.email,
            'access_token': access_token
        }
        
        return data, 200
    else:
        return 'Contraseña incorrecta'

#Metodo de registro
# @auth.route('/register', methods=['POST'])
# def register():
#     #Obtener Usuario
#     usuario = UsuarioModel.from_json(request.get_json())
#     #Verifica si el mail ya eciste en la db
#     exists = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
#     if exists:
#         return 'Email duplicado', 409
#     else:
#         try:
#             #Agregar usuario a la db
#             db.session.add(usuario)
#             db.session.commit()
#         except Exception as error:
#             db.session.rollback()
#             return str(error), 409
#         return usuario.to_json(),201
