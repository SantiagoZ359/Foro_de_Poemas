from sqlalchemy import ForeignKey
from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nota= db.Column(db.Integer(),nullable=False)
    comentario= db.Column(db.String(50), nullable=True)
    
    #relacion usuario
    usuario_id= db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)
    usuario = db.relationship('Usuario',back_populates="calificaciones",uselist=False,single_parent=True) 
    
    #relacion poema
    poema_id= db.Column(db.Integer,db.ForeignKey('poema.id'),nullable=False)
    poema = db.relationship('Poema',back_populates="calificaciones",uselist=False,single_parent = True)
    
    def __repr__(self):
        return '<Calificacion: %r %r >'% (self.nota, self.comentario, self.usuario_id, self.poema_id)
    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'nota': int(self.nota),
            'comentario': str(self.comentario),
            'usuario':self.usuario.to_json_short(),
            'poema':self.poema.to_json_short(),
        }
        return calificacion_json
    
    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'nota': self.nota,
            'usuario': self.usuario.to_json_short(),
            'comentario': str(self.comentario),
            'poema':self.poema.to_json_short(),
        }
        return calificacion_json
    
    @staticmethod
    def from_json(calificacion_json):
        id = calificacion_json.get('id')
        nota = calificacion_json.get('nota')
        comentario = calificacion_json.get('comentario')
        usuario_id = calificacion_json.get('usuario_id')
        poema_id = calificacion_json.get('poema_id')
        return Calificacion(id = id,
                        nota=nota,
                        comentario=comentario,
                        usuario_id = usuario_id,
                        poema_id= poema_id,
                        )