from flask_app import app 

#importar controlador 

from flask_app.controllers import users_controller, messages_controller

#pipenv install flask pymysql flask-bcrypt

if __name__=="__main__":
    app.run(debug=True)