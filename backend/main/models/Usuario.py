from email.policy import default
from enum import unique
from tokenize import generate_tokens
from .. import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre= db.Column(db.String(50), nullable=False)
    #Contraseña que sera el hash de la pass en txt plano
    contraseña= db.Column(db.String(50), nullable=False)
    #rol user o admin
    rol= db.Column(db.String(50), nullable=False, default = "usuario") 
    #Mail como nombre de usuario
    email= db.Column(db.String(50), unique=True, index=True, nullable=False)
    
    #relacion base
    poemas = db.relationship("Poema", back_populates="usuario",cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="usuario",cascade="all, delete-orphan")
    
    #Getter de la contraseña plana no permite leerla
    @property
    def plain_password(self):
        raise AttributeError('Contraseña no leible')
    
    #Setter de la contraseña plana no permite leerla
    #Calcula el hash y lo guarda en el atributo password
    @plain_password.setter
    def plain_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)
    
    #Metodo que compara una contraseña en texto plano con el hash guardado en la db
    def validate_pass(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)


    def __repr__(self):
        return '<Usuario: %r %r >'% (self.nombre, self.contraseña, self.rol, self.email)
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            #'contraseña': str(self.contraseña),
            #'rol':str(self.rol),
            #'email':str(self.email),
            'poemas':[poema.to_json_short() for poema in self.poemas],
            'num_poemas':len(self.poemas),
            'num_calificaciones':len(self.calificaciones),
        }
        return usuario_json
    
    def to_json_complete(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'contraseña': str(self.contraseña),
            'rol': str(self.rol),
            'email': str(self.email),
            'calificaciones': [calificacion.to_json() for calificacion in self.calificaciones], 
            'poemas' : [poema.to_json() for poema in self.poemas],


        }
        return usuario_json
    
    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
        }
        return usuario_json
    
    def to_json_short_email(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'email': str(self.email), 
            'num_calificaciones': len(self.calificaciones),
            'num_poemas': len(self.poemas),  
        }
        return usuario_json

    def to_json_short_pAm(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'num_calificaciones': len(self.calificaciones),
            'num_poemas': len(self.poemas),
        }
        return usuario_json



    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        contraseña = usuario_json.get('contraseña')
        rol = usuario_json.get('rol')
        email = usuario_json.get('email')
        return Usuario(id = id,
                        nombre=nombre,
                        plain_password = contraseña,
                        rol=rol,
                        email=email,
                        )