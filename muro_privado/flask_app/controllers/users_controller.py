from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User

#Importar el modelo de Mensaje
from flask_app.models.messages import Message

#Importación BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrate', methods=['POST'])
def registrate():
    #Validar la información ingresada
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptamos el password del usuario

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    #request.form = FORMULARIO HTML
    id = User.save(formulario) #Recibo el identificador de mi nuevo usuario

    session['user_id'] = id

    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    #Verificar que el email EXISTA
    #request.form RECIBIMOS DE HTML
    #request.form = {email: elena@cd.com, password: 123}
    user = User.get_by_email(request.form) #Recibiendo una instancia de usuario o Falso

    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/wall')



@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario) #Usuario que inicio sesión

    users = User.get_all() #Lista de TODOS los usuarios

    messages = Message.get_user_messages(formulario) #Lista con todos los mensajes de la persona que inició sesión

    return render_template('wall.html', user=user, users=users, messages=messages)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')