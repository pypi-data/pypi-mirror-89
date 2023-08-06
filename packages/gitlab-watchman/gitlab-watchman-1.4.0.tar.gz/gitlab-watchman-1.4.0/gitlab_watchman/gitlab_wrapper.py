import builtins
import calendar
import json
import os
import re
import time
import requests
import yaml
import multiprocessing
from requests.exceptions import HTTPError
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import quote

import gitlab_watchman.config as cfg
import gitlab_watchman.logger as logger


class GitLabAPIClient(object):

    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url.rstrip('\\')
        self.per_page = 100
        self.session = session = requests.session()
        session.mount(self.base_url, HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=1)))
        session.headers.update({'Authorization': 'Bearer {}'.format(self.token)})

    def make_request(self, url, params=None, data=None, method='GET', verify_ssl=True):
        try:
            relative_url = '/'.join((self.base_url, 'api/v4', url))
            response = self.session.request(method, relative_url, params=params, data=data, verify=verify_ssl)
            response.raise_for_status()

            return response

        except HTTPError as http_error:
            if response.status_code == 400:
                if response.json().get('message').get('error'):
                    raise Exception(response.json().get('message').get('error'))
                else:
                    raise http_error
            elif response.status_code == 502 or response.status_code == 500:
                print('Retrying...')
                time.sleep(30)
                response = self.session.request(method, relative_url, params=params, data=data, verify=verify_ssl)
                response.raise_for_status()

                return response
            elif response.status_code == 429:
                print('Rate limit hit, cooling off...')
                time.sleep(30)
                response = self.session.request(method, relative_url, params=params, data=data, verify=verify_ssl)
                response.raise_for_status()

                return response
            else:
                raise http_error

        except Exception as e:
            print(e)

    def get_user_by_id(self, user_id):
        return self.make_request('users/{}'.format(user_id)).json()

    def get_user_by_username(self, username):
        return self.make_request('users?username={}'.format(username)).json()

    def get_token_user(self):
        return self.make_request('user').json()

    def get_licence_info(self):
        return self.make_request('license').json()

    def get_project(self, project_id):
        return self.make_request('projects/{}'.format(project_id)).json()

    def get_variables(self, project_id):
        return self.make_request('projects/{}/variables'.format(project_id)).json()

    def get_project_members(self, project_id):
        return self.make_request('projects/{}/members'.format(project_id)).json()

    def get_file(self, project_id, path, ref):
        path = ''.join((quote(path, safe=''), '?ref=', ref))
        return self.make_request('projects/{}/repository/files/{}'.format(project_id, path)).json()

    def get_group_members(self, project_id):
        return self.make_request('groups/{}/members'.format(project_id)).json()

    def get_commit(self, project_id, commit_id):
        return self.make_request('projects/{}/repository/commits/{}'.format(project_id, commit_id)).json()

    def global_search(self, url, search_term='', search_scope=''):

        results = []
        page = 1
        params = {
            'scope': search_scope,
            'search': search_term,
            'per_page': self.per_page,
            'page': ''
        }

        response = self.make_request(url, params=params)
        page_count = response.headers.get('X-Total-Pages')

        if page_count:
            while page <= int(page_count):
                params = {
                    'scope': search_scope,
                    'search': search_term,
                    'per_page': self.per_page,
                    'page': page
                }
                r = self.make_request(url, params=params).json()
                for value in r:
                    results.append(value)
                page += 1
        else:
            params = {
                'scope': search_scope,
                'search': search_term,
            }
            r = self.make_request(url, params=params).json()
            for value in r:
                results.append(value)

        return results

    def get_all_projects(self):
        """Get all public projects. Uses keyset pagination, which currently
         is only available for the Projects resource in the GitLab API"""

        results = []

        params = {
            'pagination': 'keyset',
            'per_page': self.per_page,
            'order_by': 'id',
            'sort': 'asc'
        }

        response = self.make_request('projects', params=params)
        while 'link' in response.headers:
            next_url = response.headers.get('link')
            params = {
                'pagination': 'keyset',
                'per_page': self.per_page,
                'order_by': 'id',
                'sort': 'asc',
                'id_after': next_url.split('id_after=')[1].split('&')[0]
            }
            response = self.make_request('projects', params=params)
            for value in response.json():
                results.append(value)

        return results


def initiate_gitlab_connection():
    """Create a GitLab API client object"""

    try:
        token = os.environ['GITLAB_WATCHMAN_TOKEN']
    except KeyError:
        with open('{}/watchman.conf'.format(os.path.expanduser('~'))) as yaml_file:
            config = yaml.safe_load(yaml_file)

        token = config.get('gitlab_watchman').get('token')

    try:
        url = os.environ['GITLAB_WATCHMAN_URL']
    except KeyError:
        with open('{}/watchman.conf'.format(os.path.expanduser('~'))) as yaml_file:
            config = yaml.safe_load(yaml_file)

        url = config.get('gitlab_watchman').get('url')

    return GitLabAPIClient(token, url)


def convert_time(timestamp):
    """Convert ISO 8601 timestamp to epoch """

    pattern = '%Y-%m-%dT%H:%M:%S.%f%z'
    return int(time.mktime(time.strptime(timestamp, pattern)))


def deduplicate(input_list):
    """Removes duplicates where results are returned by multiple queries"""

    list_of_strings = [json.dumps(d) for d in input_list]
    list_of_strings = set(list_of_strings)
    return [json.loads(s) for s in list_of_strings]


def split_to_chunks(input_list, no_of_chunks):
    """Split the input list into n amount of chunks"""

    return (input_list[i::no_of_chunks] for i in range(no_of_chunks))


def find_group_owners(group_members):
    """Return all users who are both active and group Owners"""

    member_list = []
    for user in group_members:
        if user.get('state') == 'active' and user.get('access_level') == 50:
            member_list.append({
                'user_id': user.get('id'),
                'name': user.get('name'),
                'username': user.get('username'),
                'access_level': 'Owner'
            })

    return member_list


def find_user_owner(user_list):
    """Return user who owns a namespace"""

    owner_list = []
    for user in user_list:
        owner_list.append({
            'user_id': user.get('id'),
            'name': user.get('name'),
            'username': user.get('username'),
            'state': user.get('state')
        })

    return owner_list


def search(gitlab: GitLabAPIClient, log_handler, rule, scope, timeframe=cfg.ALL_TIME):
    """Uses the Search API to get search results for the given scope. These results are then split into (No of cores -
    1) number of chunks, and Multiprocessing is then used to concurrently filter them against Regex using the relevant
    worker function """

    results = []
    if isinstance(log_handler, logger.StdoutLogger):
        print = log_handler.log_info
    else:
        print = builtins.print

    for query in rule.get('strings'):
        regex = re.compile(rule.get('pattern'))
        search_result_list = gitlab.global_search('search', query, search_scope=scope)
        print('{} {} found matching search term: {}'.format(len(search_result_list), scope, query.replace('"', '')))
        result = multiprocessing.Manager().list()

        chunks = multiprocessing.cpu_count() - 1
        list_of_chunks = split_to_chunks(search_result_list, chunks)

        processes = []

        if scope == 'blobs':
            target = blob_worker
        elif scope == 'wiki_blobs':
            target = wiki_blob_worker
        elif scope == 'commits':
            target = commit_worker
        elif scope == 'issues':
            target = issue_worker
        elif scope == 'milestones':
            target = milestone_worker
        else:
            target = merge_request_worker

        for search_list in list_of_chunks:
            p = multiprocessing.Process(target=target,
                                        args=(gitlab, search_list, regex, timeframe, result))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

        results.append(list(result))

    if results:
        results = deduplicate([item for sublist in results for item in sublist])
        print('{} total matches found after filtering'.format(len(results)))
        return results
    else:
        print('No matches found after filtering')


def blob_worker(gitlab, blob_list, regex, timeframe, results):
    """Worker function for multiprocessing search of blobs. Outputs a list of matches formatted as dicts
            ready for logging """

    now = calendar.timegm(time.gmtime())
    for blob in blob_list:
        project = gitlab.get_project(blob.get('project_id'))
        file = gitlab.get_file(blob.get('project_id'), blob.get('path'), blob.get('ref'))
        if file:
            commit = gitlab.get_commit(blob.get('project_id'), file.get('last_commit_id'))
            if convert_time(commit.get('committed_date')) > (now - timeframe) and regex.search(str(blob.get('data'))):
                results_dict = {
                    'blob_id': blob.get('id'),
                    'basename': blob.get('basename'),
                    'data': blob.get('data'),
                    'path': blob.get('path'),
                    'ref_branch': blob.get('ref'),
                    'commited_date': commit.get('committed_date'),
                    'match_string': regex.search(str(blob.get('data'))).group(0),
                    'project': {
                        'project_url': project.get('web_url'),
                        'project_id': blob.get('project_id'),
                        'project_name': project.get('name'),
                        'last_activity_at': project.get('last_activity_at'),
                        'namespace': {
                            'namespace_id': project.get('namespace').get('id'),
                            'name': project.get('namespace').get('name'),
                            'kind': project.get('namespace').get('kind'),
                            'full_path': project.get('namespace').get('full_path'),
                            'parent_id': project.get('namespace').get('parent_id'),
                            'web_url': project.get('namespace').get('web_url')
                        }
                    }
                }
                if project.get('namespace').get('kind') == 'group':
                    group_members = gitlab.get_group_members(project.get('namespace').get('id'))
                    owners = find_group_owners(group_members)
                    if owners:
                        results_dict['project']['namespace']['members'] = owners
                elif project.get('namespace').get('kind') == 'user':
                    namespace_user = gitlab.get_user_by_username(project.get('namespace').get('full_path'))
                    user = find_user_owner(namespace_user)
                    if user:
                        results_dict['project']['namespace']['owner'] = user

                results.append(results_dict)

    return results


def wiki_blob_worker(gitlab, blob_list, regex, timeframe, results):
    """Worker function for multiprocessing search of wiki blobs. Outputs a list of matches formatted as dicts
            ready for logging """

    now = calendar.timegm(time.gmtime())
    for blob in blob_list:
        project = gitlab.get_project(blob.get('project_id'))
        if convert_time(project.get('last_activity_at')) > (now - timeframe) and regex.search(str(blob.get('data'))):
            results_dict = {
                'wiki_blob_id': blob.get('id'),
                'basename': blob.get('basename'),
                'data': blob.get('data'),
                'path': blob.get('path'),
                'match_string': regex.search(str(blob.get('data'))).group(0),
                'project': {
                    'project_url': project.get('web_url'),
                    'project_id': blob.get('project_id'),
                    'project_name': project.get('name'),
                    'last_activity_at': project.get('last_activity_at'),
                    'namespace': {
                        'namespace_id': project.get('namespace').get('id'),
                        'name': project.get('namespace').get('name'),
                        'kind': project.get('namespace').get('kind'),
                        'full_path': project.get('namespace').get('full_path'),
                        'parent_id': project.get('namespace').get('parent_id'),
                        'web_url': project.get('namespace').get('web_url')
                    }
                }
            }
            if project.get('namespace').get('kind') == 'group':
                group_members = gitlab.get_group_members(project.get('namespace').get('id'))
                owners = find_group_owners(group_members)
                if owners:
                    results_dict['project']['namespace']['members'] = owners
            elif project.get('namespace').get('kind') == 'user':
                namespace_user = gitlab.get_user_by_username(project.get('namespace').get('full_path'))
                user = find_user_owner(namespace_user)
                if user:
                    results_dict['project']['namespace']['owner'] = user

            results.append(results_dict)

    return results


def commit_worker(gitlab, commit_list, regex, timeframe, results):
    """Worker function for multiprocessing search of commits. Outputs a list of matches formatted as dicts
        ready for logging """

    now = calendar.timegm(time.gmtime())
    for commit in commit_list:
        if convert_time(commit.get('committed_date')) > (now - timeframe) and regex.search(str(commit.get('message'))):
            project = gitlab.get_project(commit.get('project_id'))
            results_dict = {
                'commit_id': commit.get('id'),
                'title': commit.get('title'),
                'data': commit.get('message'),
                'committed_date': commit.get('committed_date'),
                'committer_name': commit.get('committer_name'),
                'committer_email': commit.get('committer_email'),
                'match_string': regex.search(str(commit.get('message'))).group(0),
                'project': {
                    'project_url': project.get('web_url'),
                    'project_id': commit.get('project_id'),
                    'project_name': project.get('name'),
                    'last_activity_at': project.get('last_activity_at'),
                    'namespace': {
                        'namespace_id': project.get('namespace').get('id'),
                        'name': project.get('namespace').get('name'),
                        'kind': project.get('namespace').get('kind'),
                        'full_path': project.get('namespace').get('full_path'),
                        'parent_id': project.get('namespace').get('parent_id'),
                        'web_url': project.get('namespace').get('web_url')
                    }
                }
            }
            if project.get('namespace').get('kind') == 'group':
                group_members = gitlab.get_group_members(project.get('namespace').get('id'))
                owners = find_group_owners(group_members)
                if owners:
                    results_dict['project']['namespace']['members'] = owners
            elif project.get('namespace').get('kind') == 'user':
                namespace_user = gitlab.get_user_by_username(project.get('namespace').get('full_path'))
                user = find_user_owner(namespace_user)
                if user:
                    results_dict['project']['namespace']['owner'] = user

            results.append(results_dict)

    return results


def issue_worker(gitlab, issue_list, regex, timeframe, results):
    """Worker function for multiprocessing search of issues. Outputs a list of matches formatted as dicts
        ready for logging """

    now = calendar.timegm(time.gmtime())
    for issue in issue_list:
        if convert_time(issue.get('updated_at')) > (now - timeframe) and regex.search(str(issue.get('description'))):
            project = gitlab.get_project(issue.get('project_id'))
            results_dict = {
                'issue_id': issue.get('id'),
                'title': issue.get('title'),
                'description': issue.get('description'),
                'web_url': issue.get('web_url'),
                'state': issue.get('state'),
                'created_at': issue.get('created_at'),
                'updated_at': issue.get('updated_at'),
                'closed_at': issue.get('closed_at'),
                'author_id': issue.get('author').get('id'),
                'author_username': issue.get('author').get('username'),
                'due_date': issue.get('due_date'),
                'confidential': issue.get('confidential'),
                'match_string': regex.search(str(issue.get('description'))).group(0),
                'project': {
                    'project_url': project.get('web_url'),
                    'project_id': issue.get('project_id'),
                    'project_name': project.get('name'),
                    'last_activity_at': project.get('last_activity_at'),
                    'namespace': {
                        'namespace_id': project.get('namespace').get('id'),
                        'name': project.get('namespace').get('name'),
                        'kind': project.get('namespace').get('kind'),
                        'full_path': project.get('namespace').get('full_path'),
                        'parent_id': project.get('namespace').get('parent_id'),
                        'web_url': project.get('namespace').get('web_url')
                    }
                }
            }
            if issue.get('assignee'):
                results_dict['assignee_id'] = issue.get('assignee').get('id')
                results_dict['assignee_username'] = issue.get('assignee').get('username')

            if project.get('namespace').get('kind') == 'group':
                group_members = gitlab.get_group_members(project.get('namespace').get('id'))
                owners = find_group_owners(group_members)
                if owners:
                    results_dict['project']['namespace']['members'] = owners
            elif project.get('namespace').get('kind') == 'user':
                namespace_user = gitlab.get_user_by_username(project.get('namespace').get('full_path'))
                user = find_user_owner(namespace_user)
                if user:
                    results_dict['project']['namespace']['owner'] = user

            results.append(results_dict)

    return results


def milestone_worker(gitlab, milestone_list, regex, timeframe, results):
    """Worker function for multiprocessing search of milestones. Outputs a list of matches formatted as dicts
        ready for logging """

    now = calendar.timegm(time.gmtime())
    for milestone in milestone_list:
        if convert_time(milestone.get('updated_at')) > (now - timeframe) and regex.search(
                str(milestone.get('description'))):
            project = gitlab.get_project(milestone.get('project_id'))
            results_dict = {
                'milestone_id': milestone.get('id'),
                'title': milestone.get('title'),
                'description': milestone.get('description'),
                'created_at': milestone.get('created_at'),
                'updated_at': milestone.get('updated_at'),
                'due_date': milestone.get('due_date'),
                'start_date': milestone.get('start_date'),
                'match_string': regex.search(str(milestone.get('description'))).group(0),
                'project': {
                    'project_url': project.get('web_url'),
                    'project_id': milestone.get('project_id'),
                    'project_name': project.get('name'),
                    'last_activity_at': project.get('last_activity_at'),
                    'namespace': {
                        'namespace_id': project.get('namespace').get('id'),
                        'name': project.get('namespace').get('name'),
                        'kind': project.get('namespace').get('kind'),
                        'full_path': project.get('namespace').get('full_path'),
                        'parent_id': project.get('namespace').get('parent_id'),
                        'web_url': project.get('namespace').get('web_url')
                    }
                }
            }
            if project.get('namespace').get('kind') == 'group':
                group_members = gitlab.get_group_members(project.get('namespace').get('id'))
                owners = find_group_owners(group_members)
                if owners:
                    results_dict['project']['namespace']['members'] = owners
            elif project.get('namespace').get('kind') == 'user':
                namespace_user = gitlab.get_user_by_username(project.get('namespace').get('full_path'))
                user = find_user_owner(namespace_user)
                if user:
                    results_dict['project']['namespace']['owner'] = user

            results.append(results_dict)

    return results


def merge_request_worker(gitlab, merge_request_list, regex, timeframe, results):
    """Worker function for multiprocessing search of merge requests. Outputs a list of matches formatted as dicts
    ready for logging """

    now = calendar.timegm(time.gmtime())
    for merge_request in merge_request_list:
        if convert_time(merge_request.get('updated_at')) > (now - timeframe) and \
                regex.search(str(merge_request.get('description'))):
            project = gitlab.get_project(merge_request.get('project_id'))
            results_dict = {
                'merge_request_id': merge_request.get('id'),
                'title': merge_request.get('title'),
                'description': merge_request.get('description'),
                'state': merge_request.get('state'),
                'created_at': merge_request.get('created_at'),
                'updated_at': merge_request.get('updated_at'),
                'author_id': merge_request.get('author').get('id'),
                'author_username': merge_request.get('author').get('username'),
                'merge_status': merge_request.get('merge_status'),
                'url': merge_request.get('url'),
                'match_string': regex.search(str(merge_request.get('description'))).group(0),
                'project': {
                    'project_url': project.get('web_url'),
                    'project_id': merge_request.get('project_id'),
                    'project_name': project.get('name'),
                    'last_activity_at': project.get('last_activity_at'),
                    'namespace': {
                        'namespace_id': project.get('namespace').get('id'),
                        'name': project.get('namespace').get('name'),
                        'kind': project.get('namespace').get('kind'),
                        'full_path': project.get('namespace').get('full_path'),
                        'parent_id': project.get('namespace').get('parent_id'),
                        'web_url': project.get('namespace').get('web_url')
                    }
                }
            }
            if merge_request.get('assignee'):
                results_dict['assignee_id'] = merge_request.get('assignee').get('id')
                results_dict['assignee_username'] = merge_request.get('assignee').get('username')

            if project.get('namespace').get('kind') == 'group':
                group_members = gitlab.get_group_members(project.get('namespace').get('id'))
                owners = find_group_owners(group_members)
                if owners:
                    results_dict['project']['namespace']['members'] = owners
            elif project.get('namespace').get('kind') == 'user':
                namespace_user = gitlab.get_user_by_username(project.get('namespace').get('full_path'))
                user = find_user_owner(namespace_user)
                if user:
                    results_dict['project']['namespace']['owner'] = user

            results.append(results_dict)

    return results