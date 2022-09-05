def get_resource_id(name, resources):
    for resource in resources:
        if resource['displayName'] == name:
            return resource['id']
