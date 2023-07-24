import email
from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from sqlalchemy import func
from main.models import PoemaModel
from main.models import UsuarioModel
from main.models import CalificacionModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from flask_mail import Mail
from main.mail.functions import sendMail

#Usuarios

#USUARIOS = {
#    1:{'nombre-usuario': 'Carlos','nickname-usuario':'Lun891'},
#    2:{'nombre-usuario': 'Juan','nickusuario':'Juancito1991'},
#}

class Usuario(Resource):
    
    #metodo get
    
    @jwt_required(optional=True)
    def get(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        identidad_usuario = get_jwt_identity()
        if identidad_usuario:
            return usuario.to_json_short_email()
        else:
            return usuario.to_json_short()
    
    #metodo delete
    @jwt_required()
    @admin_required
    def delete(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '',204
    
    #metodo put
    @jwt_required()
    @admin_required
    def put(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key,valor in data:
            setattr(usuario,key,valor)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201


class Usuarios(Resource):
    @admin_required
    def get(self):
        pagina = 1
        por_pagina = 10
        usuarios = db.session.query(UsuarioModel)
        if request.get_json():
            filtros = request.get_json().items()
            for key, valor in filtros:
                #paginacion
                if key == "pagina":
                    pagina = int(valor)
                if key == "por_pagina":
                    por_pagina = int(valor)
                
                #filtro nombre
                if key == 'nombre':
                    usuarios = usuarios.filter(UsuarioModel.nombre.like('%'+valor+'%'))
                
                #ordenamientos
                if key == "ordenar_por":
                    #Por nombre ascendente
                    if key == 'nombre':
                        usuarios = usuarios.order_by(UsuarioModel.nombre.like('%'+valor+'%'))
                    #Por nombre descendente
                    if valor == 'npoemas[desc]':
                        usuarios = usuarios.order_by(func.count(UsuarioModel.id).desc())
                    #Por poemas ascendente
                    if valor == 'num_poemas':
                        print("Dentro")
                        usuarios = usuarios.outerjoin(UsuarioModel.calificaciones).group_by(func.count(UsuarioModel.id))
                    #Por calificaciones descendente
                    if valor == 'num_calificaciones':
                        print("dentro")
                        usuarios = usuarios.outerjoin(UsuarioModel.calificaciones).group_by(UsuarioModel.id).order_by(func.count(UsuarioModel.id).desc())


        usuarios = usuarios.paginate(pagina, por_pagina, True,18)
        return jsonify({'usuarios': [usuario.to_json_short_pAm() for usuario in usuarios.items],
                    'total':usuarios.total,
                    'paginas':usuarios.pages,
                    'pagina': pagina
                    })

    @admin_required
    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        mail_existente = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
        nombre_existente = db.session.query(UsuarioModel).filter(UsuarioModel.nombre == usuario.nombre).scalar() is not None

        if mail_existente:
            return 'Direccion de Email ya utilizada.', 409
        elif nombre_existente:
            return 'Nombre de usuario ya utilizado.', 409
        else:
            try:
                db.session.add(usuario)
                db.session.commit()
                #envio de mail

                send = sendMail([usuario.email], "Fuiste registrado en nuestro foro de poemas", 'register', usuario = usuario, rol = usuario)
            except Exception as error:
                db.session.rollback()
                return 'Formato Invalido', 409
            return usuario.to_json(),201