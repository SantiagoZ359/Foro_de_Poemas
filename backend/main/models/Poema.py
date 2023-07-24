from datetime import datetime
from statistics import mean
import statistics
from .. import db

class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    cuerpo =db.Column(db.String(500), nullable=False)
    fecha =db.Column(db.DateTime, nullable=False, default=datetime.now())

    #relacion usuario
    usuario_id = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario',back_populates="poemas", uselist=False,single_parent=True)
    
    #relacion calificacion
    calificaciones = db.relationship('Calificacion',back_populates="poema",cascade='all, delete-orphan')
    
    def __repr__(self):
        return '<Poema: %r %r >' % (self.titulo, self.usuario_id, self.cuerpo, self.fecha)
    

    #promedio de calificaciones
    #def prom_calif(self):
    #    nota_list = []
    #    if len(self.calificaciones) == 0:
    #        prom = 0
    #    else:
    #        for calificacion in self.calificaciones:
    #            nota = calificacion.nota
    #            nota_list.append(nota)
    #        prom = statistics.mean(nota_list)
    #    return prom

    def promedio_nota(self):
        notas_lista = []
        if len(self.calificaciones) == 0:
            avg = 0
        else:
            for calificacion in self.calificaciones:
                nota = calificacion.nota
                notas_lista.append(nota)
            avg = statistics.mean(notas_lista)
        return avg

    def to_json(self):   
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'cuerpo': str(self.cuerpo),
            'fecha': str(self.fecha.strftime("%d-%m-%Y")),
            'usuario': self.usuario.to_json(),
            'calificaciones': [calificacion.to_json_short() for calificacion in self.calificaciones],
            'promedio': str(self.promedio_nota()),
        }
        return poema_json

    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': self.titulo,
            'fecha': str(self.fecha.strftime("%d-%m-%Y")),
            'usuario': self.usuario.to_json_short(),
            'promedio': self.promedio_nota(),
        }
        return poema_json
    
    def to_json_public(self):
        poema_json = {
            'id': self.id,
            'titulo': self.titulo,
            'usuario':self.usuario.to_json_short(),
            'cuerpo':str(self.cuerpo),
            'fecha':str(self.fecha.strftime("%d-%m-%Y")),
            'promedio': str(self.promedio_nota()),
        }
        return poema_json

    @staticmethod
    
    #Convertir JSON a objeto
    def from_json(poema_json):
        id = poema_json.get('id')
        usuario_id = poema_json.get('usuario_id')
        titulo = poema_json.get('titulo')
        cuerpo = poema_json.get('cuerpo')
        fecha = poema_json.get('fecha')
        return Poema(id=id,
                    titulo=titulo,
                    usuario_id=usuario_id,
                    cuerpo=cuerpo,
                    fecha=fecha,
                    )
