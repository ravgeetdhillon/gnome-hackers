from flask_frozen import Freezer
from app import app
from shutil import copyfile
from helpers import load_data


freezer = Freezer(app)


@freezer.register_generator
def user_details():
    users = load_data('sorted_users_acc_days_30.json')
    for user in users:
        yield {'user_name': user['user_name']}


if __name__ == '__main__':
    freezer.freeze()
    copyfile('static/google4e1a0869f2d05873.html', 'build/google4e1a0869f2d05873.html')
