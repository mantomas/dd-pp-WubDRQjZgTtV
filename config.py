import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisisjustfordevelopment'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'todo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 2048 * 2048  # limit to 2MB upload
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    REGISTRATION_ALLOWED = True
    FILE_ALLOWED = ['png', 'jpg', 'jpeg', 'pdf', 'txt']
