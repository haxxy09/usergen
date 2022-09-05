import logging
import requests
from requests.auth import HTTPBasicAuth
import coloredlogs
from decouple import config


# LOGGING CONFIG
logger = logging.getLogger('GENERATE_IDS')

coloredlogs.install(
    fmt='[%(asctime)s %(levelname)s] %(name)s - %(message)s')


def generate_ids(count):
    baseUrl = config('DHIS2_BASE_URL')
    username = config('DHIS2_USERNAME')
    password = config('DHIS2_PASSWORD')

    url = '{0}/system/id.json?limit={1}'.format(baseUrl, count)

    try:
        logger.info('getting Ids from {}'.format(url))

        req = requests.get(url, auth=HTTPBasicAuth(username, password))
        data = req.json()

        logger.info('successfully fetched {} Ids'.format(len(data['codes'])))

        return data['codes']
    except Exception as e:
        logger.error('could not fetch Ids')
        logger.error(e)
        return []
