from flask_frozen import Freezer
from app import app
from shutil import copyfile


freezer = Freezer(app)


if __name__ == '__main__':
    freezer.freeze()
    copyfile('static/google4e1a0869f2d05873.html', 'build/google4e1a0869f2d05873.html')
