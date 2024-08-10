from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

from app import routes


'''
http://199.247.17.44:3001/users/register

'''