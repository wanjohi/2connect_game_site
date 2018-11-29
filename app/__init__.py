# third-party imports
from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    #@login_required
    def main():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Credentials. Please try again.'
            else:
                #log user in
                return redirect(url_for('main'))
        return render_template('login.html', error=error)

    @app.route("/logout")
    #@login_required
    def logout():
        logout_user()
        return redirect(url_for('main'))

    return app