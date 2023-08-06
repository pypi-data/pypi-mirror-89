from api import NextcloudAPI

class Basic(NextcloudAPI):
    headers = [{'OCS-APIRequest', 'true'}]
