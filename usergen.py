import csv
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values

config = dotenv_values(".env")

username = config['DHIS2_USERNAME']
password = config['DHIS2_PASSWORD']
base_url = config['DHIS2_BASE_URL']
filename = config['DHIS2_USERS_FILENAME']

auth = HTTPBasicAuth(username, password)

# always have a way of getting the file from
reader = tuple(csv.DictReader(open(filename)))

# TODO: environment variables need to be wired up


def generate_ids(count):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/system/id.json?limit={0}'.format(count),
                           auth=auth)
        data = req.json()
        return data['codes']
    except:
        return []


def get_users_for_group(group_id):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/userGroups/{0}.json'.format(group_id),
                           auth=auth)
        data = req.json()
        return data['users']
    except Exception as e:
        print('Could not fetch users for group id {0}'.format(group_id))
        return ''


def getResource(name, key):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/{0}.json?paging=false'.format(name),
                           auth=auth)
        data = req.json()
        resources = data[key]
        return resources
    except Exception as e:
        print('Could not fetch resource {0}'.format(name))
        return []


def createUsers(payload):
    try:
        req = requests.post('https://play.dhis2.org/2.35.1/api/metadata',
                            json=payload, auth=auth)
        print(req.json())
    except Exception as e:
        print(e)


def getUserRoles():
    return getResource('userRoles', 'userRoles')


def getOrganisationUnits():
    return getResource('organisationUnits', 'organisationUnits')


def getUserGroups():
    return getResource('userGroups', 'userGroups')


def getUserGroupUsers(id):
    return getResource('userGroups'+'/{0}'.format(0), 'users')


def getResourceId(name, resources):
    for resource in resources:
        if resource['displayName'] == name:
            return resource['id']


def create_user_groups(user_group_combos):
    groupIds = set([group["groupId"] for group in user_group_combos])
    user_groups = []

    for groupId in groupIds:
        unique_combos = filter(
            lambda x: x["groupId"] == groupId, user_group_combos)
        users_ids_in_memory = [combo["userId"] for combo in unique_combos]
        mapped_users_ids_in_memory = map(
            lambda x: {"id": x}, users_ids_in_memory)
        users = get_users_for_group(
            groupId) + mapped_users_ids_in_memory

        what_we_want = {
            "name": filter(lambda x: x["groupId"] == groupId, user_group_combos)[0]["groupName"],
            "id": groupId,
            "users": users
        }
        user_groups.append(what_we_want)
    return user_groups


def create_user_list(entries):
    organisationUnits = getOrganisationUnits()
    userGroups = getUserGroups()
    userRoles = getUserRoles()

    total_users = sum(1 for r in reader)
    user_ids = generate_ids(total_users)

    users = []
    user_group_combos = []
    for index, row in enumerate(entries):
        user_id = user_ids[index]
        user = {
            "id": user_id,
            "firstName": row['firstName'],
            "surname": row['surname'],
            "userCredentials": {
                "username": row['username'],
                "password": row['password'],
                "userRoles": [
                    {
                        "id": getResourceId(row['userRoles'], userRoles)
                    }
                ]
            },
            "organisationUnits": [
                {
                    "id": getResourceId(row['organisationUnits'], organisationUnits)
                }
            ],
            "dataViewOrganisationUnits": [
                {
                    "id": getResourceId(row['dataViewOrganisationUnits'], organisationUnits)
                }
            ]
        }

        user_group_combo = {
            "userId": user_id,
            "groupName": row["userGroups"],
            "groupId": getResourceId(row['userGroups'], userGroups)
        }

        user_group_combos.append(user_group_combo)
        users.append(user)

    return users, user_group_combos


if __name__ == '__main__':
    print('Script running ...')
    users, combos = create_user_list(reader)
    user_groups = create_user_groups(combos)
    payload = {
        "users": users,
        "userGroups": user_groups
    }
    print(payload)
    # createUsers(payload) TODO: actual creating
