from datetime import datetime, timedelta
from variables import POINTS
from PIL import Image
import dateutil.parser
import pytz
import json
import os


def days_from_now(date):
    '''
    Calculate the days from today to a past date.
    '''

    date = dateutil.parser.parse(date)
    now = pytz.utc.localize(datetime.utcnow())
    days = (now - date).days

    return days


def get_date_30_days_now():
    '''
    Get a past date which is 30 days from today.
    '''
    
    date = datetime.now() - timedelta(days=30)
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_data(file_name, directory='data'):
    '''
    Load the specified file from the given directory(optional).
    '''

    with open(f'{directory}/{file_name}', 'r') as f:
        data = json.load(f)

    return data


def save_data(data, file_name, directory='data'):
    '''
    Save the data to the specified file.
    '''

    if not os.path.exists(directory):
        os.mkdir(directory)

    with open(f'{directory}/{file_name}', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=2)


def create_user(data, method):
    '''
    Create a new user.
    '''

    new_user = {
        'id': '',
        'name': '',
        'avatar_url': '',
        'web_url': '',
        'user_name': '',
        'points': {
            'days_1': 0,
            'days_7': 0,
            'days_15': 0,
            'days_30': 0,
        },
        'awards': {
            'gold': 0,
            'silver': 0,
            'bronze': 0,
            'top10': 0,
        },
        'activity': {
            'issues': 0,
            'commits': 0,
            'merge_requests': 0,
        }
    }

    new_user = update_user_name(new_user, data, method)
    new_user = update_user_points(new_user, data, method)

    return new_user


def update_user_info(user, data):
    '''
    Update the user's info.
    '''

    user['avatar_url'] = data['avatar_url']
    user['web_url'] = data['web_url']
    user['id'] = data['id']
    user['user_name'] = data['username']
    user['name'] = user['name'].title()

    return user


def update_user_name(user, data, method):
    '''
    Update the user's name.
    '''

    if method == 'commit':
        user['name'] = data['author_name']

    elif method == 'mr':
        user['name'] = data['author']['name']

    elif method == 'issue':
        user['name'] = data['author']['name']

    return user


def update_user_points(user, data, method):
    '''
    Update the user points according to the date and method.
    '''

    if method == 'commit':

        commit = data
        commit_date = commit['created_at']
        user['activity']['commits'] += 1

        if days_from_now(commit_date) <= 1:
            user['points']['days_1'] += commit['stats']['total'] * POINTS['commit']
            user['points']['days_7'] += commit['stats']['total'] * POINTS['commit']
            user['points']['days_15'] += commit['stats']['total'] * POINTS['commit']
            user['points']['days_30'] += commit['stats']['total'] * POINTS['commit']
        elif days_from_now(commit_date) <= 7:
            user['points']['days_7'] += commit['stats']['total'] * POINTS['commit']
            user['points']['days_15'] += commit['stats']['total'] * POINTS['commit']
            user['points']['days_30'] += commit['stats']['total'] * POINTS['commit']
        elif days_from_now(commit_date) <= 15:
            user['points']['days_15'] += commit['stats']['total'] * POINTS['commit']
            user['points']['days_30'] += commit['stats']['total'] * POINTS['commit']
        elif days_from_now(commit_date) <= 30:
            user['points']['days_30'] += commit['stats']['total'] * POINTS['commit']

    elif method == 'mr':

        mr = data
        mr_date = mr['created_at']
        mr_state = mr['state']
        user['activity']['merge_requests'] += 1

        if mr_state == 'merged':
            if days_from_now(mr_date) <= 1:
                user['points']['days_1'] += POINTS['closed_mr']
                user['points']['days_7'] += POINTS['closed_mr']
                user['points']['days_15'] += POINTS['closed_mr']
                user['points']['days_30'] += POINTS['closed_mr']
            elif days_from_now(mr_date) <= 7:
                user['points']['days_7'] += POINTS['closed_mr']
                user['points']['days_15'] += POINTS['closed_mr']
                user['points']['days_30'] += POINTS['closed_mr']
            elif days_from_now(mr_date) <= 15:
                user['points']['days_15'] += POINTS['closed_mr']
                user['points']['days_30'] += POINTS['closed_mr']
            elif days_from_now(mr_date) <= 30:
                user['points']['days_30'] += POINTS['closed_mr']

        elif mr_state == 'opened':
            if days_from_now(mr_date) <= 1:
                user['points']['days_1'] += POINTS['opened_mr']
                user['points']['days_7'] += POINTS['opened_mr']
                user['points']['days_15'] += POINTS['opened_mr']
                user['points']['days_30'] += POINTS['opened_mr']
            elif days_from_now(mr_date) <= 7:
                user['points']['days_7'] += POINTS['opened_mr']
                user['points']['days_15'] += POINTS['opened_mr']
                user['points']['days_30'] += POINTS['opened_mr']
            elif days_from_now(mr_date) <= 15:
                user['points']['days_15'] += POINTS['opened_mr']
                user['points']['days_30'] += POINTS['opened_mr']
            elif days_from_now(mr_date) <= 30:
                user['points']['days_30'] += POINTS['opened_mr']

    elif method == 'issue':

        issue = data
        issue_date = issue['created_at']
        issue_state = issue['state']
        user['activity']['issues'] += 1

        if issue_state == 'opened':
            if days_from_now(issue_date) <= 1:
                user['points']['days_1'] += POINTS['opened_issue']
                user['points']['days_7'] += POINTS['opened_issue']
                user['points']['days_15'] += POINTS['opened_issue']
                user['points']['days_30'] += POINTS['opened_issue']
            elif days_from_now(issue_date) <= 7:
                user['points']['days_7'] += POINTS['opened_issue']
                user['points']['days_15'] += POINTS['opened_issue']
                user['points']['days_30'] += POINTS['opened_issue']
            elif days_from_now(issue_date) <= 15:
                user['points']['days_15'] += POINTS['opened_issue']
                user['points']['days_30'] += POINTS['opened_issue']
            elif days_from_now(issue_date) <= 30:
                user['points']['days_30'] += POINTS['opened_issue']

        elif issue_state == 'closed':
            if days_from_now(issue_date) <= 1:
                user['points']['days_1'] += POINTS['closed_issue']
                user['points']['days_7'] += POINTS['closed_issue']
                user['points']['days_15'] += POINTS['closed_issue']
                user['points']['days_30'] += POINTS['closed_issue']
            elif days_from_now(issue_date) <= 7:
                user['points']['days_7'] += POINTS['closed_issue']
                user['points']['days_15'] += POINTS['closed_issue']
                user['points']['days_30'] += POINTS['closed_issue']
            elif days_from_now(issue_date) <= 15:
                user['points']['days_15'] += POINTS['closed_issue']
                user['points']['days_30'] += POINTS['closed_issue']
            elif days_from_now(issue_date) <= 30:
                user['points']['days_30'] += POINTS['closed_issue']
    
    user['points']['days_1'] = round(user['points']['days_1'])
    user['points']['days_7'] = round(user['points']['days_7'])
    user['points']['days_15'] = round(user['points']['days_15'])
    user['points']['days_30'] = round(user['points']['days_30'])

    return user


def compress_image(image_name):
    '''
    Reduce the image file size by reducing the image dimensions to 80x80.    
    '''

    image = Image.open(f'static/img/users/{image_name}.png')
    x = min(48, image.size[0])
    image = image.resize((x, x), Image.LANCZOS)
    image.save(f'static/img/users/{image_name}_small.png', optimize=True, quality=95)
