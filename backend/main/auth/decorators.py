from tabnanny import verbose
from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

#Decorador para restringir el acceso a los admins
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        #cerificar que el JWT es correcto
        verify_jwt_in_request()
        #Obtener claims de adentro del JWT
        claims = get_jwt()
        #Verifica que el rol sea admin
        if claims['rol'] == 'admin':
            #ejecuta func
            return fn(*args, **kwargs)
        else:
            return 'Solo los administradores pueden acceder', 403
    return wrapper

#define el atributo que se utilizara para identificar el user
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    #Define id como atributo identificatorio
    return usuario.id

#define que atributos se guardaran dentro del token
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'rol': usuario.rol,
        'id': usuario.id,
        'email': usuario.email
    }
    return claims