from flask import Blueprint, url_for, render_template, make_response, request, current_app
import requests, json
import json

app = Blueprint('app', __name__, url_prefix='/')

def get_poem(id, jwt=None):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    if jwt:
        headers = get_headers(jwt)

    else:
        headers = get_headers(without_token=True)
    return requests.get(api_url, headers=headers)

def get_poems_by_id(id, page=1, perpage=3):
    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"page": page, "perpage": perpage, "usuario_id": id}

    headers = get_headers(without_token=True)
    return requests.get(api_url, json=data, headers=headers)

def get_poems(jwt=None, page=1, perpage=3):
    api_url = f'{current_app.config["API_URL"]}/poemas'
    data = {"pagina": page, "por_pagina": perpage}

    if jwt:
        headers = get_headers(jwt=jwt)
    else:
        headers = get_headers(without_token=True)
    return requests.get(api_url, json=data, headers=headers)

def get_poems_page():
    return request.cookies.get("poems_page")

def get_user_info(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers,)

def get_user(id):
    api_url = f'{current_app.config["API_URL"]}/usuario/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)

def json_load(response):
    return json.loads(response.text)

def get_headers(without_token=False, jwt=None):
    if jwt is None and not without_token:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {get_jwt()}"}
    if jwt and not without_token:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type": "application/json"}

def get_jwt():
    return request.cookies.get("access_token")

def get_id():
    return request.cookies.get("id")

def get_username(user_id):
    headers = get_headers()
    api_url = f'{current_app.config["API_URL"]}/usuario/{user_id}'
    response = requests.get(api_url, headers=headers)
    user = json.loads(response.text)
    return user["nombre"]

def add_poem(api_url, titulo, contenido):
    data = {"titulo": titulo, "contenido": contenido}
    headers = get_headers()
    return requests.post(api_url, json=data, headers=headers)

def login(email, contraseña):
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    data = {"email": email, "contraseña": contraseña}
    headers = get_headers(without_token=True)

    return requests.post(api_url, json=data, headers=headers)

def get_json(resp):
    return json.loads(resp.text)

def get_marks_by_poem_id(id):
    api_url = f'{current_app.config["API_URL"]}/calificaciones'

    data = {"poema_id": id}
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)

def get_marks_by_poet_id(id):
    api_url = f'{current_app.config["API_URL"]}/calificaciones'

    data = {"usuario_id": id}   
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)

def get_poems_page():
    return request.cookies.get("poems_page")
