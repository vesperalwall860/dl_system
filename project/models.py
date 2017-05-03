from flask_login import UserMixin
from sqlalchemy.orm import class_mapper, ColumnProperty
from werkzeug import check_password_hash, generate_password_hash

from . import db, login_manager


class ColsMapMixin(object):
    @classmethod
    def columns(cls):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [prop.key for prop in \
            class_mapper(cls).iterate_properties \
            if isinstance(prop, ColumnProperty)]


class User(UserMixin, ColsMapMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    bad_logins = db.Column(db.Integer)
    last_attempt = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))