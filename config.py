import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask app configuration"""

    # for production SECRET_KEY env. variable must be set
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisisjustfordevelopment'
    # will use sqlite DB (not for production!) if env. not set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'todo.db')
    # SQAlchemy event system silenced for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # limit to 2MB upload
    MAX_CONTENT_LENGTH = 2048 * 2048
    # folder will be created upon first upload
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    # False to disable registration
    REGISTRATION_ALLOWED = True
    # list of allowed file extensions to download
    FILE_ALLOWED = ['png', 'jpg', 'jpeg', 'pdf', 'txt']
