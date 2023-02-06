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

    def get_info(self):
        self.ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        try:
            self.info = self.ydl.extract_info(self.url,
                                              download=self.download)
        except DownloadError:
            self.info = None
            raise ProviderError("Cannot get info")

    @staticmethod
    @interfacedoc
    def id():
        return "youtube"

    @staticmethod
    @interfacedoc
    def name():
        return "YouTube"

    @staticmethod
    @interfacedoc
    def description():
        return "YouTube provider"

    @staticmethod
    @interfacedoc
    def domain():
        return "www.youtube.com"

    @staticmethod
    @interfacedoc
    def access():
        return True

    @interfacedoc
    def exists(self):
        return True if self.info else False

    @interfacedoc
    def get_title(self):
        return self.info['title']

    @interfacedoc
    def set_id_from_url(self):
        self.id = self.url.split("?v=")[-1:][0]

    @interfacedoc
    def set_url_from_id(self):
        self.url = "https://www.youtube.com/watch?v=" + self.id

    @interfacedoc
    def get_audio(self):
        try:
            file_path = self.ydl.prepare_filename(self.info)
            source_uri = self.info['formats'][0]['url']

            if self.download:
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                # removing file extension
                file_path = os.path.splitext(file_path)[0]
                # searching for file with same name and replacing extension
                file_name = os.path.relpath(file_path, self.path)
                for file in os.listdir(self.path):
                    if file_name == os.path.splitext(file)[0]:
                        file_path += os.path.splitext(file)[1]
                return file_path
            else:
                return source_uri
        except DownloadError:
            raise ProviderError("Cannot get source")


