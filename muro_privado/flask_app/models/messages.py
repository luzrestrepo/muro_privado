from flask_app.config.mysqlconnection import  connectToMySQL

class Message:

    def __init__(self, data):
        #data = {id: 1, content: "Hola", creat.., up.., rec_id.., send_id.., receiver_name: "Pedro", sender_name:"Barack"}
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']

        #2 propiedades extra que vamos a obtener gracias al LEFT JOIN
        self.sender_name = data['sender_name']
        self.receiver_name = data['receiver_name']


    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s)"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        return result

    @classmethod
    def get_user_messages(cls, formulario):
        #formulario = {id: 1}
        #2 LEFT JOINS
        query = "SELECT messages.*, receivers.first_name as receiver_name, senders.first_name as sender_name FROM messages LEFT JOIN users as receivers ON receivers.id = receiver_id LEFT JOIN users as senders ON senders.id = sender_id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('muro_privado').query_db(query, formulario) #Lista de diccionarios
        messages = []
        for message in results:
            #message = {id: 1, content: "Hola", creat.., up.., rec_id.., send_id.., receiver_name: "Pedro", sender_name:"Barack"}
            messages.append(cls(message)) #1.- cls(message) me crea instancia de mensaje. 2.- Agregamos la instancia a la lista de mensajes

        return messages

    @classmethod
    def eliminate(cls, formulario):
        #formulario = {id: 1}
        query = "DELETE FROM messages WHERE id = %(id)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        return result