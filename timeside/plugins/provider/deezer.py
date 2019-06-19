from timeside.core import implements, interfacedoc
from timeside.core.provider import Provider
from timeside.core.api import IProvider

import os
from requests import get

class Deezer(Provider):
    """Deezer Provider"""
    implements(IProvider)
    
    @staticmethod
    @interfacedoc
    def id():
        return 'deezer'

    @staticmethod
    @interfacedoc
    def name():
        return "Deezer Plugin"

    def get_source_id(self, external_id, path, download=False):
        request_url = 'https://api.deezer.com/track/' + external_id
        request_json = get(request_url).json()
        source_uri = request_json['preview']
        if download:
            file_name = request_json['artist']['name'] + '-' + request_json['title_short'] + '-' + external_id
            file_name = file_name.replace(' ','_')  + '.mp3'
            file_path = os.path.join(path,file_name)
            r = get(source_uri)
            with open(file_path,'wb') as f:
                f.write(r.content)
                f.close()
            return file_path
        else:
            return source_uri
    
    def get_source_url(self, url, path, download=False):
        deezer_track_id = url.split("/")[-1:]
        return self.get_source_id(deezer_track_id, path, download)