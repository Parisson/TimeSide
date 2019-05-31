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

    def get_source(self, url, path, download=False):
        deezer_track_id = url.split("/")[-1:]
        request_url = 'https://api.deezer.com/track/' + deezer_track_id[0]
        request_json = get(request_url).json()
        source_uri = request_json['preview']
        if download:
            file_name = request_json['artist']['name'] + '-' + request_json['title_short'] + '-' + deezer_track_id[0]
            file_name = file_name.replace(' ','_')  + '.mp3'
            file_path = os.path.join(path,file_name)
            r = get(source_uri)
            with open(file_path,'wb') as f:
                f.write(r.content)
                f.close()
            return file_path
        else:
            return source_uri