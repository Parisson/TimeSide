from timeside.core import implements, interfacedoc
from timeside.core.provider import Provider
from timeside.core.api import IProvider
from timeside.core.exceptions import ProviderError

import youtube_dl
from youtube_dl.utils import DownloadError
import os


class YouTube(Provider):
    """YouTube audio Provider based on Youtube DL"""
    implements(IProvider)

    def __init__(self, url=None, id=None, path=None, download=False):
        self.url = url
        self.id = id
        self.path = path
        self.download = download

        if not self.url or self.id:
            raise AttributeError("A URL or an ID must be given")

        self.ydl_opts = {
            'format': 'bestaudio',
            'verbose': False,
            'cachedir': False,
            'outtmpl': self.path + '%(title)s-%(id)s.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio'}],
            'restrictfilenames': True,
            'force-ipv4': True,
        }

        self.get_info()

    @staticmethod
    @interfacedoc
    def id():
        return "youtube"

    @staticmethod
    @interfacedoc
    def name():
        return "YouTube Plugin"

    @staticmethod
    @interfacedoc
    def resource_access():
        return True

    # @interfacedoc
    # def get_source_from_url(self, ext_uri, path, download=False):
    #     return self.get_source(
    #         path, ext_uri=ext_uri, download=download
    #         )

    # @interfacedoc
    # def get_source_from_id(self, ext_id, path, download=False):
    #     return self.get_source(
    #         path, ext_id=ext_id, download=download
    #         )

    def resource_exists(self):
        return True if self.info else False

    def get_info(self):
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        try:
            self.info = self.ydl.extract_info(self.url,
                                              download=self.download)
        except DownloadError:
            self.info = None

    def get_title(self):
        return self.info['title']

    def get_source(self):
        file_path = ydl.prepare_filename(self.info)
        source_uri = info['formats'][0]['url']

        if self.download:
            if not os.path.exists(self.path):
                os.makedirs(path)
            # removing file extension
            file_path = os.path.splitext(file_path)[0]
            # searching for file with same name and replacing extension
            file_name = os.path.relpath(file_path, path)
            for file in os.listdir(path):
                if file_name == os.path.splitext(file)[0]:
                    file_path += os.path.splitext(file)[1]
            return file_path
        else:
            return source_uri

    @interfacedoc
    def get_id_from_url(self):
        with youtube_dl.YoutubeDL({}) as ydl:
            try:
                info = ydl.extract_info(self.url, download=False)
                return info['id']
            except DownloadError:
                raise ProviderError(self.id(), external_uri=self.url)



