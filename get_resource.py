import logging
import requests
from requests.auth import HTTPBasicAuth
import coloredlogs
from decouple import config


# LOGGING CONFIG
logger = logging.getLogger('GET_RESOURCE')

coloredlogs.install(
    fmt='[%(asctime)s %(levelname)s] %(name)s - %(message)s')


def get_resource(name, key):
    baseUrl = config('DHIS2_BASE_URL')
    username = config('DHIS2_USERNAME')
    password = config('DHIS2_PASSWORD')

    url = '{0}/{1}.json?paging=false'.format(baseUrl, name)

    try:
        logger.info('getting resources from {}'.format(url))

        req = requests.get(url, auth=HTTPBasicAuth(username, password))
        data = req.json()

        logger.info('successfully fetched {}'.format(name))

        return data[key]
    except Exception as e:
        logger.error('could not fetch {0}'.format(name))
        logger.error(e)
        return []
