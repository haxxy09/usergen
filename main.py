import json
import pandas as pd
from decouple import config
import coloredlogs
import logging
from get_resource import get_resource
from generate_ids import generate_ids
from get_resource_id import get_resource_id

# LOGGING CONFIG
logger = logging.getLogger('MAIN')

coloredlogs.install(
    fmt='[%(asctime)s %(levelname)s] %(name)s - %(message)s')

if __name__ == '__main__':
    logger.info("Script running... 😊⏳")

    # TODO: variables
    DHIS2_USERNAME = config('DHIS2_USERNAME')
    DHIS2_PASSWORD = config('DHIS2_PASSWORD')
    fileName = config('DHIS2_USERS_FILENAME')
    chunkSize = int(config('CHUNK_SIZE'))

    organisation_units = get_resource('organisationUnits', 'organisationUnits')
    user_groups = get_resource('userGroups', 'userGroups')
    user_roles = get_resource('userRoles', 'userRoles')

    logger.info('{} organisation units fetched'.format(
        len(organisation_units)))
    logger.info('{} user groups fetched'.format(len(user_groups)))
    logger.info('{} user roles fetched'.format(len(user_roles)))

    with pd.read_csv(fileName, iterator=False, chunksize=chunkSize) as reader:
        for chunkIndex, chunk in enumerate(reader):
            logger.info('processing chunk #: {} 🤪'.format(chunkIndex + 1))
            logger.info('chunk has {} rows'.format(len(chunk)))

            users = []
            user_group_combos = []
            generatedUserIds = generate_ids(len(chunk))
            idsIndex = 0

            for index, row in chunk.iterrows():
                logger.info('processing row number {} rows'.format(index + 1))

                user_id = generatedUserIds[idsIndex]

                user_roles_split = row[4].split(", ")
                organisation_units_split = row[6].split(", ")
                data_view_organisation_units_split = row[7].split(", ")
                user_groups_split = row[5].split(", ")

                user = {
                    "id": user_id,
                    "firstName": row[0],
                    "surname": row[1],
                    "userCredentials": {
                        "username": row[2],
                        "password": row[3],
                        "userRoles": list(
                            map(lambda x: {
                                "id": get_resource_id(x, user_roles)
                            }, user_roles_split)
                        )
                    },
                    "organisationUnits": list(
                        map(lambda x: {
                            "id": get_resource_id(x, organisation_units)
                        }, organisation_units_split)),
                    "dataViewOrganisationUnits": list(
                        map(lambda x: {
                            "id": get_resource_id(x, organisation_units)
                        }, data_view_organisation_units_split)),
                    "userGroupCombo": {
                        "userId": user_id,
                        "groupName": user_groups_split,
                        "groupId": list(map(lambda x: get_resource_id(x, user_groups), user_groups_split)),
                    }
                }

                users.append(user)
                idsIndex += 1

            with open('usersBatch_{}.json'.format(chunkIndex + 1), 'w') as f:
                json.dump(users, f)
