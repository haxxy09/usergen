import csv
import requests
from requests.auth import HTTPBasicAuth
# from dhis2 import generate_uid


# always have a way of getting the file from
reader = csv.DictReader(open("test_users.csv"))


def generate_ids(count):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/system/id.json?limit={0}'.format(count),
                           auth=HTTPBasicAuth('admin', 'district'))
        data = req.json()
        return data['codes']
    except:
        return []


def get_users_for_group(group_id):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/userGroups/{0}.json'.format(group_id),
                           auth=HTTPBasicAuth('admin', 'district'))
        data = req.json()
        return data['users']
    except Exception as e:
        print('Could not fetch users for group id {0}'.format(group_id))
        return ''


def getResource(name, key):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/{0}.json?paging=false'.format(name),
                           auth=HTTPBasicAuth('admin', 'district'))
        data = req.json()
        resources = data[key]
        return resources
    except Exception as e:
        print('Could not fetch resource {0}'.format(name))
        return []


def createUsers(users):
    try:
        data = {
            "users": users
        }
        req = requests.post('https://play.dhis2.org/2.35.1/api/metadata',
                            json=data, auth=HTTPBasicAuth('admin', 'district'))
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
    return getResource('userGroups'+'/{}'.format({id}), 'users')


def getResourceId(name, resources):
    for resource in resources:
        if resource['displayName'] == name:
            return resource['id']


organisationUnits = getOrganisationUnits()
userGroups = getUserGroups()
userRoles = getUserRoles()

total_users = sum(1 for r in reader)
user_ids = generate_ids(total_users)

userGroups = []


def create_user_list():
    users = []
    for row in reader:
        print(row)
        # for index, row in enumerate(reader):
        #     print('Index ' + str(index))
        #     user = {
        #         "id": user_ids[index],
        #         "firstName": row['firstName'],
        #         "surname": row['surname'],
        #         "userCredentials": {
        #             "username": row['username'],
        #             "password": row['password'],
        #             "userRoles": [
        #                 {
        #                     "id": getResourceId(row['userRoles'], userRoles)
        #                 }
        #             ]
        #         },
        #         "organisationUnits": [
        #             {
        #                 "id": getResourceId(row['organisationUnits'], organisationUnits)
        #             }
        #         ],
        #         "dataViewOrganisationUnits": [
        #             {
        #                 "id": getResourceId(row['dataViewOrganisationUnits'], organisationUnits)
        #             }
        #         ]
        #     }
        #     users.append(user)
        # return users

# Testing


# _users = get_users_for_group('wl5cDMuUhmF')
# print(_users)

# createUsers(users)

create_user_list()
