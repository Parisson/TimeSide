#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import timeside
import magic
from timeside.core import *


class TestAnalyzers(Component):
    analyzers = processors(timeside.analyze.IAnalyzer)

    def list(self):
        analyzers = []
        for analyzer_class in self.analyzers:
            # FIXME: should access the name, id and unit member statically
            # there should be no need to instantiate analyzer_class
            # eg: access directly analyzer_class.name(), etc...
            #
            # This remark is true at many places in this file
            analyzer = analyzer_class()
            analyzers.append({'name':analyzer.name(),
                            'id':analyzer.id(),
                            'unit':analyzer.unit(),
                            })
        print analyzers

    def run(self, media):
        print '\n=== Analyzer testing ===\n'
        for analyzer_class in self.analyzers:
            analyzer = analyzer_class()
            id = analyzer.id()
            value = analyzer.render(media)
            print id + ' = ' + str(value) + ' ' + analyzer.unit()


class TestDecoders(Component):
    decoders = processors(timeside.decode.IDecoder)

    def list(self):
        decoders_list = []
        for decoder_class in self.decoders:
            decoder = decoder_class()
            decoders_list.append({'format': decoder.format(),
                            'mime_type': decoder.mime_type(),
                            'file_extension': decoder.file_extension(),
                            })
        print decoders_list

    def get_decoder(self, mime_type):
        for decoder_class in self.decoders:
            decoder = decoder_class()
            if decoder.mime_type() == mime_type:
                return decoder

    def export(self, media_dir):
        files = os.listdir(media_dir)
        for file in files:
            media = media_dir + os.sep + file
            mime = mimetype(media)
            print mime
            file_ext = file.split('.')[-1]
            decoder = self.get_decoder(mime)
            if decoder:
                stream = decoder.process(media)
                #print decoder.command
                file_path = 'results/sweep' + '_' + file_ext + '.wav'
                f = open(file_path, 'w')
                for chunk in stream:
                    f.write(chunk)
                    f.flush()
                f.close()

class TestEncoders(Component):
    encoders = processors(timeside.encode.IEncoder)

    def list(self):
        encoders = []
        for encoder_class in self.encoders:
            encoder = encoder_class()
            encoders.append({'format': encoder.format(),
                            'mime_type': encoder.mime_type(),
                            })
        print encoders

    def get_encoder(self, mime_type):
        for encoder_class in self.encoders:
            encoder = encoder_class()
            if encoder.mime_type() == mime_type:
                return encoder

    def run(self, source, metadata):
        print '\n=== Encoder testing ===\n'
        for encoder_class in self.encoders:
            encoder = encoder_class()
            mime = mimetype(source)
            format = encoder.format()
            decoders = TestDecoders()
            decoder = decoders.get_decoder(mime)
            decoded = decoder.process(source)
            ext = encoder.file_extension()
            stream = encoder.process(decoded, metadata)
            file_path = 'results/sweep' + '.' + ext
            file = open(file_path, 'w')
            for chunk in stream:
                file.write(chunk)
            print 'Sound exported to :' + file_path
            file.close()


class TestGraphers(Component):
    graphers = processors(timeside.graph.IGrapher)

    def list(self):
        graphers = []
        for grapher_class in self.graphers:
            grapher = grapher_class()
            graphers.append({'id':grapher.id(),
                            'name':grapher.name(),
                            })
        print graphers

    def run(self, media):
        print '\n=== Grapher testing ===\n'
        for grapher_class in self.graphers:
            grapher = grapher_class()
            id = grapher.id()
            image = grapher.render(media)
            file_path = 'results/'+id+'.png'
            file = open(file_path, 'w')
            for chunk in image:
                file.write(chunk)
            print 'Image exported to :' + file_path
            file.close()

def mimetype(path):
    if hasattr(magic, "Magic"):
        if not hasattr(mimetype, "magic"):
            mimetype.magic = magic.Magic(mime=True)
        magic_file = mimetype.magic.from_file(path)
        mime = magic_file.lower()
    else:
        if not hasattr(mimetype, "magic"):
            mimetype.magic = magic.open(magic.MAGIC_MIME)
            mimetype.magic.load()
        mime = mimetype.magic.file(path).lower()

    return mime

if __name__ == '__main__':
    sample = 'samples/sweep_source.wav'
    metadata = (('creator', 'yomguy'), ('date', '2009'), ('name', 'test'))
    a = TestAnalyzers()
    d = TestDecoders()
    e = TestEncoders()
    g = TestGraphers()
    a.list()
    d.list()
    e.list()
    g.list()
    a.run(sample)
    g.run(sample)
    e.run(sample, metadata)
    d.export('samples/')


