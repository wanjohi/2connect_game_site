from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

# silly user model
class User(UserMixin, db.Model):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)