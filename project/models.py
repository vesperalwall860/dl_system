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


custom_learn_courses = db.Table('custom_learn_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class User(UserMixin, ColsMapMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    learn_courses = db.relationship('Course', secondary=custom_learn_courses,
                                    backref=db.backref('students',
                                                       lazy='dynamic'))
    courses = db.relationship('Course', backref='user', lazy='dynamic')
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


class Course(ColsMapMixin, db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Category(ColsMapMixin, db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(127))
    courses = db.relationship('Course', backref='category', lazy='dynamic')
    children = db.relationship('Category')
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Lesson(ColsMapMixin, db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(127))
    text = db.Column(db.Text)
    files = db.relationship('File', lazy='dynamic')
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    chat = db.relationship('Chat', uselist=False,
                            backref='guarantee_of_payment')


class File(ColsMapMixin, db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(256))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))


class Chat(ColsMapMixin, db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    messages = db.relationship('ChatMessage', backref='chat', lazy='dynamic')


class ChatMessage(ColsMapMixin, db.Model):
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime, default=datetime.now())