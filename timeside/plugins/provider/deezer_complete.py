from timeside.core import implements, interfacedoc
from timeside.core.provider import Provider
from timeside.core.api import IProvider
from timeside.core.tools.utils import slugify

import os
from requests import get


class DeezerComplete(Provider):
    """Deezer Plugin representing complete tracks on Deezer's infrastructure"""
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
    def description():
        return "Deezer complete provider"

    @staticmethod
    @interfacedoc
    def domain():
        return "www.deezer.com"

    @staticmethod
    @interfacedoc
    def access():
        return False

    @interfacedoc
    def exists(self):
        return True

    @interfacedoc
    def get_title(self):
        return

    @interfacedoc
    def get_file(self):
        return

    @interfacedoc
    def set_id_from_url(self):
        return self.url.split("/")[-1:][0]

    @interfacedoc
    def set_url_from_id(self):
        return
