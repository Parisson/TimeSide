from timeside.core import implements, interfacedoc
from timeside.core.provider import Provider
from timeside.core.exceptions import ProviderError
from timeside.core.api import IProvider
from timeside.core.tools.utils import slugify

import os
from requests import get
import json


class DeezerPreview(Provider):
    """Deezer Plugin to retrieve deezer's 30 seconds tracks preview"""

    implements(IProvider)

    def __init__(self, url=None, id=None, download=False, path=""):
        self.url = url
        self.id = id
        self.path = path
        self.download = download
        self.info = None

        if not self.url and not self.id:
            raise AttributeError("A URL or an ID must be given")
        elif self.id and not self.url:
            self.set_url_from_id()
        elif not self.id and self.url:
            self.set_id_from_url()

        self.get_info()

    def get_info(self):
        try:
            request = get(self.url)
            assert request.status_code == 200
        except AssertionError:
            raise ProviderError('deezer_preview', external_id=self.id)

        self.request_dict = json.loads(request.content)

    @staticmethod
    @interfacedoc
    def id():
        return 'deezer_preview'

    @staticmethod
    @interfacedoc
    def name():
        return "Deezer Preview"

    @staticmethod
    @interfacedoc
    def description():
        return "Deezer preview provider"

    @staticmethod
    @interfacedoc
    def domain():
        return "www.deezer.com"

    @staticmethod
    @interfacedoc
    def access():
        return True

    @interfacedoc
    def exists(self):
        return True

    @interfacedoc
    def set_id_from_url(self):
        self.id = self.url.split("/")[-1:][0]

    @interfacedoc
    def set_url_from_id(self):
        self.url = 'https://api.deezer.com/track/' + self.id

    @interfacedoc
    def get_title(self):
        return self.info['title']

    @interfacedoc
    def get_file(self):
        source_uri = self.request_dict['preview']
        if self.download:
            file_name = self.request_dict['artist']['name'] + '-' + self.request_dict['title_short'] + '-' + self.id
            file_name = slugify(file_name) + '.mp3'
            file_path = os.path.join(path,file_name)
            r = get(source_uri)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(file_path,'wb') as f:
                f.write(r.content)
                f.close()
            return file_path
        else:
            return source_uri

