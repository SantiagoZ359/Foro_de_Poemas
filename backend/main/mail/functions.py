from .. import mailsender
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException

#Se crea la funcion para el envio de emails
def sendMail(to, subject, template, **kwargs):
    #configuro el email
    msg = Message( subject, sender = current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        #creamos el cuerpo del mensaje.
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        #enviamos el email
        result = mailsender.send(msg)
    except SMTPException as e:
        print(str(e))
        return "Envio de mail fallado"
    return True
    