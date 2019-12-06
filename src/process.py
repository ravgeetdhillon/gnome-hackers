from helpers import load_data, create_user, save_data, days_from_now, update_user_points, update_user_info
from fetch import fetch_images
import json


def process_commits(users, commits):
    '''
    Process the commits and award users points.
    '''

    for commit in commits:
        for user in users:
            if set(commit['author_name'].split()).issubset( set(user['name'].split()) ):
                user = update_user_points(user, commit, 'commit')
                break
        else:
            new_user = create_user(commit, 'commit')
            users.append(new_user)

    return users


def process_merge_requests(users, merge_requests):
    '''
    Process the merge requests and award users points.
    '''

    for mr in merge_requests:
        for user in users:
            if set(user['name'].split()).issubset( set(mr['author']['name'].split()) ):
                user = update_user_points(user, mr, 'mr')
                break
        else:
            new_user = create_user(mr, 'mr')
            users.append(new_user)

    return users


def process_issues(users, issues):
    '''
    Process the issues and award users points.
    '''

    for index, issue in enumerate(issues):

        if issue['state'] == 'closed':
                        
            for user in users:
                if issue['closed_by'] is not None:
                    if set(user['name'].split()).issubset( set(issue['closed_by']['name'].split()) ):
                        user = update_user_points(user, issue, 'issue')
                        break
                else:
                    break
            else:
                new_user = create_user(issue, 'issue')
                users.append(new_user)

        elif issue['state'] == 'opened':

            for user in users:
                if issue['author'] is not None:
                    if set(user['name'].split()).issubset( set(issue['author']['name'].split()) ):
                        user = update_user_points(user, issue, 'issue')
                        break
                else:
                    break
            else:
                new_user = create_user(issue, 'issue')
                users.append(new_user)

    return users


def process_users(users, all_users):
    '''
    Process the users and update their Gitlab related information.
    '''

    for user in users:
        for user_data in all_users:
            if set(user['name'].split()).issubset( set(user_data['name'].split()) ):
                user = update_user_info(user, user_data)

    return users


def main():
    '''
    Main function for the process.py.
    '''

    # initialize the users array to store the data about the users contributing to the GNOME
    users = []

    # load the commits, merge requests and issues
    commits = load_data('commits.json')
    merge_requests = load_data('merge_requests.json')
    issues = load_data('issues.json')
    all_users = load_data('users.json')

    # process the commits, merge requests and issues and generate points for the users
    users = process_issues(users, issues)
    users = process_merge_requests(users, merge_requests)
    users = process_commits(users, commits)
    users = process_users(users, all_users)

    # download the avatar image from each user
    fetch_images(users)

    # sort the data for each criteria and save them in their respective json files
    criteria = ['days_1', 'days_7', 'days_15', 'days_30']
    
    for key in criteria:
        users = sorted(users, key=lambda k: k['points'][key], reverse=True)
        save_data(users, f'sorted_users_acc_{key}.json')


if __name__ == '__main__':
    main()