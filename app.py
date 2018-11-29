from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# db variable initialization
db = SQLAlchemy()
db.init_app(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route("/")
@login_required
def main():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            id = 1
            user = User(id)
            login_user(user)
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run()