import os
import random
import string
import grp
import pwd

from werkzeug.utils import secure_filename

from .. import config


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in config['production'].ALLOWED_EXTENSIONS


def pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def photo_file_name_santizer(photo):
    filename = secure_filename(photo.data.filename)

    if filename and allowed_file(filename):
        filename = str(random.randint(100000, 999999)) + filename
        filepath = os.path.join(config['production'].UPLOAD_FOLDER, filename)
        photo.data.save(filepath)

        # Give the uploaded file read rights to everyone
        uid = pwd.getpwnam("medipay2").pw_uid
        gid = grp.getgrnam("nobody").gr_gid
        os.chown(filepath, uid, gid)

    if not filename:
        filename = ''

    if filename:
        photo_filename = '/static/uploads/' + filename
    else:
        photo_filename = '/static/img/person-solid.png'

    return photo_filename


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of str


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of bytes
