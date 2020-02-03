from timeside.core import implements, interfacedoc
from timeside.core.provider import Provider
from timeside.core.api import IProvider
from timeside.core.tools.utils import slugify

import os
from requests import get


class DeezerComplete(Provider):
    """
    Represents Deezer Provider while loading results
    computed on complete tracks on Deezer's infrastructure
    """
    implements(IProvider)
   
    @staticmethod
    @interfacedoc
    def id():
        return 'deezer_complete'

    @staticmethod
    @interfacedoc
    def name():
        return "Deezer Complete"

    @staticmethod
    @interfacedoc
    def ressource_access():
        return False

    def get_source_from_id(self, external_id, path, download=False):
        return ''
            
    def get_source_from_url(self, url, path, download=False):
        return ''

    def get_id_from_url(self, url):
        return url.split("/")[-1:][0]
