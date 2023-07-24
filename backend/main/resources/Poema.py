from flask_restful import Resource
from flask import request, jsonify
import jwt
from .. import db
from main.models import PoemaModel
from main.models import UsuarioModel
from main.models import CalificacionModel
from sqlalchemy import func
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

class Poema(Resource):
    @jwt_required(optional=True)
    def get(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        identidad = get_jwt_identity()
        
        if identidad:
            return poema.to_json()
        else:
            return poema.to_json_public()

    @jwt_required()
    def delete(self, id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        identidad_usuario = get_jwt_identity()
        claims = get_jwt()

        if claims['rol'] == "admin" or poema.usuario_id == identidad_usuario:
            try:
                db.session.delete(poema)
                db.session.commit()
            except Exception as error:
                return 'Formato incorrecto', 204
            return '', 201
        else:
            return 'No tienes permiso para realizar esta acción.', 403

class Poemas(Resource):
    @jwt_required(optional=True)
    def get(self):
        claims = get_jwt()
        
        if (not claims):
            return self.show_poems_without_token()

        if claims['rol'] in ["usuario", "admin"]:
            return self.show_poems_with_token(user_id=claims['id'])
        else:
            return 'Not "rol" found.', 403

    def show_poems_without_token(self):
        page = request.args.get("page", default=1, type=int)
        perpage = request.args.get("perpage", default=3, type=int)

        poemas = db.session.query(PoemaModel)
        poemas_pagination = poemas.paginate(page=page, per_page=perpage, error_out=False)

        return jsonify({
            "poemas": [poema.to_json() for poema in poemas_pagination.items],
            "total": poemas_pagination.total,
            "pages": poemas_pagination.pages,
            "page": page
        })


    def show_poems_with_token(self, user_id):
        page = 1
        perpage = 3

        poems = db.session.query(PoemaModel).filter(PoemaModel.usuario_id != int(user_id)).order_by(PoemaModel.fecha).outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.count(CalificacionModel.nota))

        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "page":
                    page = int(value)
                if key == "perpage":
                    perpage = int(value)
        poems_pagination = poems.paginate(page, perpage, False)

        return jsonify({
            "poems": [poem.to_json() for poem in poems_pagination.items],
            "total": poems_pagination.total,
            "pages": poems_pagination.pages,
            "page": page
        })

    @jwt_required()
    def post(self):
        if request.cookies.get('access_token'):
            r = requests.get()
        poema = PoemaModel.from_json(request.get_json())
        identidad_usuario = get_jwt_identity()
        poema.usuario_id = identidad_usuario
        usuario = db.session.query(UsuarioModel).get(identidad_usuario)
        claims = get_jwt()

        if len(usuario.poemas) == 0 or len(usuario.calificaciones) / len(usuario.poemas) >= 0 and claims['rol'] != "admin":
            try:
                db.session.add(poema)
                db.session.commit()
            except Exception as error:
                return 'Formato incorrecto', 400
            return poema.to_json(), 201
        else:
            return 'Antes debes calificar 5 poemas para subir uno nuevo. (Los administradores no pueden subir poemas)', 404
