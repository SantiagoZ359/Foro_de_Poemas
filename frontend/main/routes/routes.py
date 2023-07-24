from email import header
from flask import Blueprint, render_template, make_response, request, current_app, url_for, redirect,flash
from . import functions as f
from . import auth
import requests
import json


app = Blueprint('app', __name__, url_prefix= '/')

@app.route('/poeta', methods=['GET', 'POST'])
def index_poeta(jwt = None):
    jwt =f.get_jwt() 
    if jwt:   
        response = f.get_poems()
        print(response)
        poems = json.loads(response.text)
        poems = f.get_json(response)
        poem_list = poems["poemas"]
        user = f.get_user(f.get_id())
        user = json.loads(user.text)
        print(user)
        return render_template('pag_princ_poeta.html', poems = poem_list, user = user, jwt = jwt) 
    else:
        return render_template("login.html")
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Obtener password y email
        email = request.form.get("email")
        password = request.form.get("contraseña")
        
        if email != "" and password != "":
            response = f.login(email, password)
            
            try:
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                # Guardar el token en las cookies y devuelve la página.
                resp = make_response(redirect(url_for('app.index_poeta')))
                #resp = make_response(redirect(url_for('main.index'), token))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp
            except json.JSONDecodeError:
                return render_template("login.html", error="Respuesta inválida del servidor")
        flash("Your credentials are incorrect!", 'error')
        return render_template("login.html", error="Credenciales incorrectas")
    else:
        return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def index_user():
    #api_url = f'{current_app.config["API_URL"]}/poemas'
    # Paginacion
    try:
        page = int(request.form.get('n_page'))
    except:
        page = request.form.get("n_page")
        if (page == "< Atras"):
            page = int(f.get_poems_page()) - 1
        elif (page == "Siguiente >"):
            page = int(f.get_poems_page()) + 1
        else:
            page = f.get_poems_page()
            if (page == None):
                page = 1
            else:
                page = int(page)
    
    response = f.get_poems()
    print(response)
    poems = json.loads(response.text)
    poems = f.get_json(response)
    poem_list = poems["poemas"]
    # Verificar si la clave 'poems' existe en la respuesta
    return render_template('pag_princ_user.html', poems = poem_list)


@app.route('/editar_perfil')
def editar_perfil():
    return render_template ('editar_perfil.html')

@app.route('/lista_poem_user')
def lista_poemas_usuario():
    return render_template ('lista_poem_user.html')

@app.route('/lista_poema_poeta')
def lista_poem_poeta():
    return render_template ('lista_poema_poeta.html')

@app.route('/perfil')
def details():
    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        # Guardamos la información de usuario en una variable.
        user_info_response = f.get_user_info(user["id"])
        user_info_text = user_info_response.text # Obtener el contenido de la respuesta como cadena de texto
        user_info = json.loads(user_info_text)
        print(user_info)
        return render_template('perfil.html', jwt=jwt, user_info=user_info)
    else:
        return redirect(url_for('app.login'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            title = request.form['titulo']
            body = request.form['cuerpo']
            print(title)
            print(body)
            id = f.get_id()
            print(id)
            data = {"usuario_id": id, "titulo": title, "cuerpo": body}
            headers = f.get_headers(without_token=False)
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poemas', json=data, headers=headers)
                print(response)
                if response.ok:
                    response = f.json_load(response)
                    return redirect(url_for('app.view_user', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('app.create'))
            else:
                return redirect(url_for('app.create'))
        else:
            #Mostrar template
            return render_template('subir_poema.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('app.login'))

@app.route('/ver_poema/<int:id>')
def view_user(id):
    if request.cookies.get('access_token'):
        jwt = f.get_jwt()
        user_id = int(f.get_id())
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        resp = f.get_marks_by_poem_id(id)
        marks = json.loads(resp.text)
        print(marks)
        #Mostrar template
        return render_template('ver_poema_poeta.html', jwt = jwt, poem = poem, marks = marks)
    else:
        poem = f.get_poem(id)
        poem = json.loads(poem.text)
        mark = f.get_marks_by_poem_id(id)
        marks = json.loads(mark.text)
        print(marks)
        #Mostrar template
        
        return render_template('ver_poema_user.html', poem = poem, marks = marks)

    
@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("app.login")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp

@app.route('/mis_poemas')
def mis_poemas():
    jwt = f.get_jwt()
    if jwt:
        user = auth.load_user(jwt)
        resp = f.get_poems_by_id(user["id"])
        poems = json.loads(resp.text)
        poemsList = poems["poemas"]
        return render_template('lista_poema_poeta.html', jwt=jwt, poems = poemsList)
    else:
        return redirect(url_for('app.login'))

# @app.route('/mis_calificaciones')
# def mis_calif():
#     jwt = f.get_jwt()
#     if jwt:
#         user = auth.load_user(jwt)
#         user_id = str(user["id"])
#         resp = f.get_marks_by_poet_id(str(user_id))
#         marks = json.loads(resp.text)
#         poem = f.get_poem(marks["poema_id"])
#         poem = json.loads(poem.text)
#         return render_template('a.html', jwt=jwt, marks = marks, poem = poem)
#     else:
#         return redirect(url_for('app.login'))

@app.route('/ver_poema/<int:id>', methods=['GET', 'POST'])
def add_mark(id):
    jwt = f.get_jwt()
    if jwt:
        if request.method == 'POST':
            score = request.form['inlineRadioOptions']
            commentary = request.form['commentary']
            user_id = f.get_id()
            data = {"usuario_id": user_id, "poema_id": id, "nota": score, "comentario": commentary}
            print(data)
            headers = f.get_headers(without_token=False)
            if score != "" and commentary != "":
                response = requests.post(f'{current_app.config["API_URL"]}/calificaciones', json=data, headers=headers)
                print(response)
                if response.ok:
                    return redirect(url_for('app.view_user', id=id, jwt=jwt))
                else:
                    return redirect(url_for('app.add_mark', id=id))
            else:
                return redirect(url_for('app.add_mark', id=id))
        else:
            #Mostrar template
            return render_template('ver_poema_poeta.html', jwt=f.get_jwt())
    else:
        return redirect(url_for('app.login'))