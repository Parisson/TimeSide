from timeside.core import implements, interfacedoc
from timeside.core.provider import Provider
from timeside.core.api import IProvider

import youtube_dl
import os


class YouTube(Provider):
    """YouTube audio Provider using youtube-dl"""
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

    def get_source_from_url(self, url, path, download=False):
        return self.get_source(url, path, download)

    def get_source_from_id(self, external_id, path, download=False):
        return self.get_source(external_id, path, download)

    def get_source(self, url, path, download=False):
        ydl_opts = {
                    'format': 'bestaudio',
                    'verbose': False,
                    'cachedir': False,
                    'outtmpl': path + '%(title)s-%(id)s.%(ext)s',
                    'postprocessors': [{'key':'FFmpegExtractAudio'}],
                    'restrictfilenames':True,
                }
        if not os.path.exists(path):
                os.makedirs(path)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=download)
            file_path = ydl.prepare_filename(info)            
            source_uri = info['formats'][0]['url']

        if download:
            #removing file extension
            file_path = os.path.splitext(file_path)[0]
            #searching for file with same name and replacing extension
            file_name = os.path.relpath(file_path,path)
            for file in os.listdir(path):
                if file_name == os.path.splitext(file)[0]:
                    file_path += os.path.splitext(file)[1]
            return file_path
        else:
            return source_uri
    
    def get_id_from_url(self, url):
        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['id']
            
