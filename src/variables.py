import os

GITLAB_SERVER = 'https://gitlab.gnome.org'
PRIVATE_TOKEN = os.environ.get('GITLAB_PRIVATE_TOKEN')

POINTS = {
    'commit': 0.01,
    'opened_mr': 5,
    'closed_mr': 10,
    'opened_issue': 1,
    'closed_issue': 2,
}

SITE_CONFIG = {
    'title': 'GNOME Hackers',
    'tagline': 'Leaderboard for hackers contributing to the GNOME',
    'description': 'A Leaderboard web app for hackers contributing to the projects hosted by GNOME.',
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
