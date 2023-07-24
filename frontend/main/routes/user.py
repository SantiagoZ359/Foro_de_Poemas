from flask import Blueprint, render_template, json, request
from . import functions as f
from . import auth

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/details/<int:id>')
def details(id):
    if request.cookies.get('access_token'):

        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)

        return render_template('perfil.html',user = user)
    else:
        return render_template('login.html')

@user.route('/edit_profile')
def edit_profile():
    if request.cookies.get('access_token'):

        user = f.get_user_info(id)
        user = json.loads(user.text)
        print(user)

        return render_template('editar_perfil.html',user = user)
    else:
        return render_template('login.html')