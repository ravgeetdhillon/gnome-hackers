from helpers import save_data, get_date_30_days_now
from variables import GITLAB_SERVER, PRIVATE_TOKEN
import requests
import gitlab
import json
import time
import os


def fetch_users(gl):
    '''
    Download all the users on the https://gitlab.gnome.org.
    '''
    
    start = time.time()
    print('Fetching users.')

    users = gl.users.list(all=True)
    users = [user.attributes for user in users]
    save_data(users, 'users.json')
    print(f'Downloaded and saved {len(users)} users.')

    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')


def fetch_groups(gl):
    '''
    Download all the groups on the https://gitlab.gnome.org.
    '''

    start = time.time()
    print('Fetching groups.')

    # donot include the `Archive` group
    blacklist = [4001]

    groups = json.loads(requests.get('https://gitlab.gnome.org/api/v4/groups', params={'per_page': 100}).text)
    save_data(groups, 'groups.json')
    print(f'Downloaded and saved {len(groups)} groups.')

    # create a list of group_ids for downloading the projects in the each group
    group_ids = []
    for group in groups:
        if group['id'] not in blacklist:
            group_ids.append(group['id'])

    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')

    return group_ids


def fetch_projects(gl, group_ids):
    '''
    Download all the projects on the https://gitlab.gnome.org.
    '''

    start = time.time()
    print('Fetching projects.')

    # get the all the projects in each group
    projects = []
    for group_id in group_ids:
        group = gl.groups.get(id=group_id, lazy=True)
        group_projects = group.projects.list(all=True)
        projects += group_projects

    projects = [project.attributes for project in projects]

    save_data(projects, 'projects.json')
    print(f'Downloaded and saved {len(projects)} projects.')

    # create a list of project_ids for downloading the issues, merge_requests, commits in the each project
    project_ids = []
    for project in projects:
        project_ids.append(project['id'])

    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')

    return project_ids


def fetch_projects_data(gl, project_ids):
    '''
    Download all the merge requests, issues and commits for each project on the https://gitlab.gnome.org.
    '''

    start = time.time()
    print('Fetching merge requests, issues and commits.')

    merge_requests = []
    issues = []
    commits = []

    for index, project_id in enumerate(project_ids):

        print(index, end=', ')
        project = gl.projects.get(id=project_id, lazy=True)

        since = get_date_30_days_now()

        try:
            project_merge_requests = project.mergerequests.list(all=True, query_parameters={'state': 'all', 'created_after': since})
            merge_requests += project_merge_requests
        except Exception as e:
            print(f'{e}. Raised while getting merge requests.')

        try:
            project_issues = project.issues.list(all=True, query_parameters={'created_after': since})
            issues += project_issues
        except Exception as e:
            print(f'{e}. Raised while getting issues.')

        try:
            project_commits = project.commits.list(all=True, query_parameters={'since': since})
        except Exception as e:
            print(f'{e}. Raised while getting commits.')

        for commit in project_commits:
            commit = commit.attributes
            commit = gl.projects.get(id=commit['project_id'], lazy=True).commits.get(id=commit['id'])
            commits.append(commit)

    merge_requests = [merge_request.attributes for merge_request in merge_requests]
    issues = [issue.attributes for issue in issues]
    commits = [commit.attributes for commit in commits]

    save_data(merge_requests, 'merge_requests.json')
    print(f'Downloaded and saved {len(merge_requests)} merge requests.')

    save_data(issues, 'issues.json')
    print(f'Downloaded and saved {len(issues)} issues.')

    save_data(commits, 'commits.json')
    print(f'Downloaded and saved {len(commits)} commits.')

    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')


def fetch_images(users):
    '''
    Download the user avatars.
    '''
    
    start = time.time()

    if not os.path.exists('static/img/users'):
        os.mkdir('static/img/users')

    for user in users:
        try:
            image = requests.get(user['avatar_url'])
            with open(f'static/img/users/{user["id"]}.png', 'wb') as f:
                f.write(image.content)
        except Exception as e:
            print(e)

    finish = time.time()
    print(f'Took {round(finish-start, 2)} seconds.')


def main():
    '''
    Main function for the fetch.py.
    '''

    # create a gitlab object and authenticate it
    gl = gitlab.Gitlab(GITLAB_SERVER, private_token=PRIVATE_TOKEN)
    gl.auth()

    # fetch the groups and get their group ids
    group_ids = fetch_groups(gl)

    # fetch the projects in each group and get their project ids
    project_ids = fetch_projects(gl, group_ids)

    # fetch the project's merge requests, issues and commits
    fetch_projects_data(gl, project_ids)

    # fetch all the users on the GNOME Gitlab instance
    fetch_users(gl)


if __name__ == '__main__':
    main()
