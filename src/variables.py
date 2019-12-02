import os

GITLAB_SERVER = 'https://gitlab.gnome.org'
PRIVATE_TOKEN = os.environ.get('GITLAB_PRIVATE_TOKEN')

POINTS = {
    'commit': 1,
    'opened_mr': 500,
    'closed_mr': 1000,
    'opened_issue': 100,
    'closed_issue': 200,
}

SITE_CONFIG = {
    'title': 'GNOME Hackers',
    'tagline': 'Leaderboard for hackers contributing to the GNOME',
    'description': 'A Leaderboard web app for hackers contributing to the projects managed by GNOME.',
    'author': {
        'name': 'Ravgeet Dhillon',
        'website': 'https://ravgeetdhillon.github.io/',
        'facebook': 'https://facebook.com/ravgeet.dhillon/',
        'twitter': 'https://twitter.com/ravgeetdhillon/',
        'twitter_username': 'ravgeetdhillon',
    },
    'github': 'https://github.com/ravgeetdhillon/gnome-hackers',
    'url': '',
    'img': '',
}