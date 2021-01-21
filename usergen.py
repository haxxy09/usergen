import csv
import requests
from requests.auth import HTTPBasicAuth

# always have a way of getting the file from
reader = csv.DictReader(open("test_users.csv"))
users = []

# TODO: Need to make sure the DHIS2 username and password are dynamic
def getResource(name, key):
    try:
        req = requests.get('https://play.dhis2.org/2.35.1/api/{0}.json?paging=false'.format(name),
                           auth=HTTPBasicAuth('admin', 'district'))
        data = req.json()
        resources = data[key]
        return resources
    except Exception as e:
        print('Could not resource {0}'.format(name))
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


def getResourceId(name, resources):
    for resource in resources:
        if resource['displayName'] == name:
            return resource['id']


organisationUnits = getOrganisationUnits()
userGroups = getUserGroups()
userRoles = getUserRoles()

print(userGroups)

for row in reader:
    user = {
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
        ],
        "userGroups": [
            {
                "id": getResourceId(row['userGroups'], userGroups)
            }
        ]
    }
    users.append(user)

createUsers(users)
