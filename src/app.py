from flask import Flask, render_template
from variables import SITE_CONFIG
from helpers import load_data


app = Flask(__name__)


@app.route('/')
def index():

    users = load_data('sorted_users_acc_days_1.json')
    users_days_1 = users[:10]
    users = load_data('sorted_users_acc_days_7.json')
    users_days_7 = users[:10]
    users = load_data('sorted_users_acc_days_15.json')
    users_days_15 = users[:10]
    users = load_data('sorted_users_acc_days_30.json')
    users_days_30 = users[:10]
    
    data = {
        'page': {
            'stats': [
                {
                    'type': 'Today',
                    'key': 'days_1',
                    'users': users_days_1,
                },
                {
                    'type': 'Week',
                    'key': 'days_7',
                    'users': users_days_7,
                },
                {
                    'type': 'Fortnight',
                    'key': 'days_15',
                    'users': users_days_15,
                },
                {
                    'type': 'Month',
                    'key': 'days_30',
                    'users': users_days_30,
                },
            ]
        },
        'site': SITE_CONFIG
    }

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
