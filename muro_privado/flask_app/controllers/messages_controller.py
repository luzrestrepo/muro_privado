from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importacion del modelo de message 

from flask_app.models.messages import Message

@app.route ('/send_message' , methods=['POST'])
def send_message():
    if 'user_id'not in session:
        return redirect('/')

#Guardar el mensaje.request.form =diccionario con todos los campos del formulario         

    Message.save(request.form)    
    return('/wall')


@app.route ('/eliminar/mensaje/<int:id>')   #en mi url voy a obtener ID 
def eliminar_mansaje(id):
    formulario = {"id" : id} 
    Message.eliminate(formulario)
    return redirect ('/wall')