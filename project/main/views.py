from flask import flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from . import main
from .helpers import pass_generator, photo_file_name_santizer
from .services import UserService
from .. import config, create_app, db, redis_store, models
from .. import auth
from ..auth.forms import LoginForm
from ..auth.views import login_validation
from ..models import User


user_service = UserService()


@main.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        form = LoginForm()

        if form.validate_on_submit():
            return login_validation(form)

        return render_template('auth/login.html', form=form)

    return render_template('index.html')