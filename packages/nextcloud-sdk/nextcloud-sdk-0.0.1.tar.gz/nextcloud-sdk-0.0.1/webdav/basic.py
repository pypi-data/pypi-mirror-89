from collections import OrderedDict
from api import NextcloudAPI
from decimal import Decimal
from io import BytesIO
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import xmltodict


class Basic(NextcloudAPI):

    props_dict = {
        'getlastmodified': 'd',
        'getetag': 'd',
        'getcontenttype': 'd',
        'resourcetype': 'd',
        'getcontentlength': 'd',
        'id': 'oc',
        'fileid': 'oc',
        'favorite': 'oc',
        'comments-href': 'oc',
        'comments-count': 'oc',
        'comments-unread': 'oc',
        'owner-id': 'oc',
        'owner-display-name': 'oc',
        'share-types': 'oc',
        'checksums': 'oc',
        'size': 'oc',
        'has-preview': 'nc',
        'rich-workspace': 'nc'
    }

    # PROPFIND remote.php/dav/files/user/path/to/folder
    def list(self, username:str, path_to_folder='', **props):
        """
        Request parameters Example:
            <?xml version="1.0"?>
                <d:propfind  xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
                <d:prop>
                        <d:getlastmodified />
                        <d:getetag />
                        <d:getcontenttype />
                        <d:resourcetype />
                        <oc:fileid />
                        <oc:permissions />
                        <oc:size />
                        <d:getcontentlength />
                        <nc:has-preview />
                        <oc:favorite />
                        <oc:comments-unread />
                        <oc:owner-display-name />
                        <oc:share-types />
                </d:prop>
                </d:propfind>

        All properties:
            * {DAV:}getlastmodified
            * {DAV:}getetag
            * {DAV:}getcontenttype
            * {DAV:}resourcetype
            * {DAV:}getcontentlength
            * {http://owncloud.org/ns}id The fileid namespaced by the instance id, globally unique
            * {http://owncloud.org/ns}fileid The unique id for the file within the instance
            * {http://owncloud.org/ns}favorite
            * {http://owncloud.org/ns}comments-href
            * {http://owncloud.org/ns}comments-count
            * {http://owncloud.org/ns}comments-unread
            * {http://owncloud.org/ns}owner-id The user id of the owner of a shared file
            * {http://owncloud.org/ns}owner-display-name The display name of the owner of a shared file
            * {http://owncloud.org/ns}share-types
            * {http://owncloud.org/ns}checksums
            * {http://nextcloud.org/ns}has-preview
            * {http://owncloud.org/ns}size Unlike getcontentlength, this property also works for folders reporting the size of everything in the folder.
            * {http://nextcloud.org/ns}rich-workspace this property is provided by the text app
        """

        url = self.host + '/remote.php/dav/files' + '/' + username + '/' + path_to_folder
        params = self._make_request_params({
            'getlastmodified': True,
            'getetag': True,
            'getcontenttype': True,
            'resourcetype': True,
            'getcontentlength': True,
            'favorite':True,
            'size':True, 
        })

        resp = requests.request('PROPFIND', url, 
            auth=HTTPBasicAuth(self.username, self.password), data=params)
        resp_text = resp.text
        folder_content = self._ls(resp_text)
        return folder_content

    # GET remote.php/dav/files/user/path/to/file
    def download(self, path_to_file:str):
        url = self.host + path_to_file
        resp = requests.request('GET', url, auth=HTTPBasicAuth(self.username, self.password))
        return BytesIO(resp.content)

    # PUT remote.php/dav/files/user/path/to/file
    def upload(self, filebytes, username:str, path_to_file:str):
        """
            A file can be uploading by sending a PUT request to the file 
            and sending the raw file contents as the request body.
        """
        url = self.host + '/remote.php/dav/files/' + username + path_to_file
        resp = requests.request('PUT', url, auth=HTTPBasicAuth(self.username, self.password), data=filebytes)
        return resp.text

    def create_folder(self, username, path_to_new_folder:str):
        """
            Create a folder
        """
        url = self.host + '/' + username + '/' + path_to_new_folder
        resp = requests.request('MKCOL', url, auth=HTTPBasicAuth(self.username, self.password))

    def delete_file_or_folder(self, username, path_to_file:str):
        """
            Delete a file or folder recursively
        """
        url = self.url + '/' + username + '/' + path_to_file
        resp = requests.request('MKCOL', url, auth=HTTPBasicAuth(self.username, self.password))


    # -------------- list part start ----------------
    def _ls(self, resp_text)->list:
        folder_contents = []
        resp_dict = xmltodict.parse(resp_text)
        filesAndFolders = resp_dict['d:multistatus']['d:response']
        if len(filesAndFolders) < 2:
            return folder_contents
        else:
            for i in range(1, len(filesAndFolders)):
                file = filesAndFolders[i]
                propstats = file['d:propstat']
                href = file['d:href']
                is_folder = False

                if type(propstats) is OrderedDict:
                    # 当只有一个子元素的时候解析为collections.OrderedDict
                    folder_contents.append(self._get_propstats_info(propstats, href, is_folder))
                else:
                    # 有多个子元素的时候解析为list
                    for propstat in propstats:
                        item=self._get_propstats_info(propstat, href, is_folder)
                        if item is not None:
                            folder_contents.append(item)
            return folder_contents

    def _get_propstats_info(self, propstat, href, is_folder):
        if propstat['d:status'] == 'HTTP/1.1 200 OK':
            props = propstat['d:prop']
            contenttype = props.get('d:contenttype')
            lastmodified = props.get('d:getlastmodified')
            size = int(props.get('oc:size', '0'))
            human_readable_size = self._humanize_unit(size)
            if contenttype is None:
                # Is Folder
                is_folder = True
                end_index = href.rfind('/')
                start_index = href.rfind('/',0,end_index)+1
                filename = href[start_index:end_index]
            else:
                filename = href[href.rfind('/')+1:]
            item = {
                'filename': filename,
                'href': href,
                'is_folder': is_folder,
                'content_type': contenttype,
                'last_modified': lastmodified,
                'size': size,
                'human_readable_size': human_readable_size
            }
            return item
        return None

    def _humanize_unit(self, size) -> str:
        units = ['Byte', 'KB', 'MB', 'GB', 'TB', 'PB']
        power_of_1024 = 0
        while power_of_1024 < len(units):
            if size % (1024 ** power_of_1024) < 1024 :
                break
            else:
                power_of_1024 += 1
        num = Decimal(str(size / (1024 ** power_of_1024))).quantize(Decimal('0.01'), rounding='ROUND_HALF_UP')
        return ' '.join([str(num), units[power_of_1024]])
        
    def _make_request_params(self, props):
        if len(props) < 1:
            return None
        dom_props = []
        for key in props.keys():
            value = self.props_dict.get(key)
            if value is not None:
                dom_props.append(':'.join([value, key]))

        root = ET.Element('d:propfind', attrib={
            'xmlns:d': 'DAV:', 
            'xmlns:oc': 'http://owncloud.org/ns',
            'xmlns:nc': 'http://nextcloud.org/ns'
            })

        dprop = ET.SubElement(root, 'd:prop')

        for prop in dom_props:
            ET.SubElement(dprop, prop)

        return ET.tostring(root, 'utf-8')
    # -------------- list part end ----------------