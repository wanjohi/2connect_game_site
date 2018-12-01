from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    '''
    User model
    '''
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_activated = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    ais = db.relationship('Ai', backref='user', lazy=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Ai(db.Model):
    """
    Ai model
    """
    __tablename__ = 'ais'

    id = db.Column(db.Integer, primary_key=True)
    uploaded_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(60), unique=True)



class GameLog(db.Model):
    """
    Game logs model
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_draw = db.Column(db.Boolean, default=False)
    ai_won_id = db.Column(db.Integer, db.ForeignKey('ais.id'), nullable=False)
    ai_lost_id = db.Column(db.Integer, db.ForeignKey('ais.id'), nullable=False)
    ai_won = db.relationship('Ai', backref='games_won', foreign_keys=[ai_won_id], lazy=True)
    ai_lost = db.relationship('Ai', backref='games_lost', foreign_keys=[ai_lost_id], lazy=True)
    log_link = db.Column(db.String(255), nullable=False)