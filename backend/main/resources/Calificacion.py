from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel
from main.models import UsuarioModel
from main.models import PoemaModel
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from flask_mail import Mail
from main.mail.functions import sendMail

#Calificaciones

#CALIFICACIONES = {
#    1:{'calificacion': '8','Autor':'Lun891'},
#    2:{'calificacion': '10','Autor':'Juancito1991'},
#}

class Calificacion(Resource):
    def get(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()
    
    @jwt_required()
    def delete(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        identidad_usuario = get_jwt_identity()
        calificacion.calificacionId = identidad_usuario
        claims = get_jwt()
        if calificacion.usuario_id == identidad_usuario or claims['rol'] == "admin":
            try:
                db.session.delete(calificacion)
                db.session.commit()
            except Exception as error:
                return 'Formato Invalido', 204
            return 'Eliminado', 201
        else:
            return 'No tienes permisos para realizar esta accion.', 403
    
    @jwt_required()
    def put(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        identidad_usuario = get_jwt_identity()
        calificacion.calificacionId = identidad_usuario
        if calificacion.usuario_id == identidad_usuario:
            try:
                data = request.get_json().items()
                for key, valor in data:
                    setattr(calificacion,key,valor)
                db.session.add(calificacion)
                db.session.commit()
            except Exception as error:
                return 'Formato Invalido', 204
            return calificacion.to_json(), 201
        else:
            return 'No tienes permiso para realizar esta accion.', 403

class Calificaciones(Resource):
    def get (self):
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == "poema_id":
                    return self.show_marks_by_poem_id(value)
                elif key == "poeta_id":
                    return self.show_marks_by_poet_id(value)
                            
        calificaciones = db.session.query(CalificacionModel).all()
        return jsonify ([calificacion.to_json_short() for calificacion in calificaciones])

    def show_marks_by_poem_id(self, id):
        calificacion = db.session.query(CalificacionModel)
        calificaciones = calificacion.filter(CalificacionModel.poema.has(PoemaModel.id == id)).all()
        return jsonify(
            [calificacion.to_json() for calificacion in calificaciones]
        )
    def show_marks_by_poet_id(self, id):
        calificacion = db.session.query(UsuarioModel)
        calificaciones = calificacion.filter(CalificacionModel.poema.has(UsuarioModel.id == id)).all()
        return jsonify(
            [calificacion.to_json() for calificacion in calificaciones]
        )

    @jwt_required()
    def post(self):
        
        calificacion = CalificacionModel.from_json(request.get_json())
        identidad_usuario = get_jwt_identity()
        calificacion.calificacionId = identidad_usuario
        claims = get_jwt()
        #creo la variable usuario donde traigo cual usuario es igual al id de identidad_usuario
        
        usuario = db.session.query(UsuarioModel).get(identidad_usuario)
        if usuario and claims["rol"] != "admin":
            try:
                db.session.add(calificacion)
                db.session.commit()
                #parte de email, entre los [] esta el email del user que realizo la calificacion
                send = sendMail([calificacion.poema.usuario.email],"Tu poema recibio una calificacion",'calificado',usuario1 = usuario, usuario = calificacion.poema.usuario, poema = calificacion.poema )
            except Exception as error:
                db.session.rollback()
                return 'Formato incorrecto', 409
        else:
            return 'No dispones de permisos para realizar esta accion.!', 403