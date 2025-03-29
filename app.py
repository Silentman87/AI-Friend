from flask import Flask, render_template, redirect, url_for, request, flash, Response
import flask
from flask_login import LoginManager, login_manager
import flask_login
from flask_login.utils import login_required, login_user, logout_user
from requests import session
from datetime import datetime, timedelta
from flask import jsonify
from flask_login import current_user
from flask import session


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def login():
    return render_template('index.html')



@app.route('/register', methods = ['GET'])
def register() :
    return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def home() :
    return render_template('home.html')




if __name__ == "__main__" :
    app.run(debug=True)