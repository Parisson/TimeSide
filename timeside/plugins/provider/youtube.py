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
    def ressource_access():
        return True

    @interfacedoc
    def get_source_from_url(self, ext_uri, path, download=False):
        return self.get_source(
            path, ext_uri=ext_uri, download=download
            )

    @interfacedoc
    def get_source_from_id(self, ext_id, path, download=False):
        return self.get_source(
            path, ext_id=ext_id, download=download
            )

    def get_source(self, path, ext_id=None, ext_uri=None, download=False):
        ydl_opts = {
                    'format': 'bestaudio',
                    'verbose': False,
                    'cachedir': False,
                    'outtmpl': path + '%(title)s-%(id)s.%(ext)s',
                    'postprocessors': [{'key': 'FFmpegExtractAudio'}],
                    'restrictfilenames': True,
                }
        ref = ext_id or ext_uri
        if not ref:
            raise AttributeError("an external id or uri must be given")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(ref, download=download)
            except DownloadError:
                raise ProviderError(
                            self.id(),
                            external_id=ext_id,
                            external_uri=ext_uri
                            )
            file_path = ydl.prepare_filename(info)
            source_uri = info['formats'][0]['url']

        if download:
            if not os.path.exists(path):
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
    def get_id_from_url(self, url):
        with youtube_dl.YoutubeDL({}) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return info['id']
            except DownloadError:
                raise ProviderError(self.id(), external_uri=url)
