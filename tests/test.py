#!/usr/bin/python
# -*- coding: utf-8 -*-

import timeside
from timeside.core import Component, ExtensionPoint, ComponentManager


class TestAnalyzers(Component):
    analyzers = ExtensionPoint(timeside.analyze.IAnalyzer)

    def list(self):
        analyzers = []
        for analyzer in self.analyzers:
            analyzers.append({'name':analyzer.name(),
                            'id':analyzer.id(),
                            'unit':analyzer.unit(),
                            })
        print analyzers

    def run(self, media):
        print '\n=== Analyzer testing ===\n'
        for analyzer in self.analyzers:
            id = analyzer.id()
            value = analyzer.render(media)
            print id + ' = ' + str(value) + ' ' + analyzer.unit()


class TestDecoders(Component):
    decoders = ExtensionPoint(timeside.decode.IDecoder)

    def list(self):
        decoders = []
        for decoder in self.decoders:
            decoders.append({'format':decoder.format(),
                            'mime_type':decoder.mime_type(),
                            })
        print decoders

    def run(self, media, format):
        for decoder in self.decoders:
            if decoder.format() == format:
                break
        return decoder.process(media)


class TestEncoders(Component):
    encoders = ExtensionPoint(timeside.encode.IEncoder)

    def list(self):
        encoders = []
        for encoder in self.encoders:
            encoders.append({'format':encoder.format(),
                            'mime_type':encoder.mime_type(),
                            })
        print encoders

    def run(self, source, metadata):
        print '\n=== Encoder testing ===\n'
        for encoder in self.encoders:
            format = encoder.format()
            ext = encoder.file_extension()
            stream = encoder.process(source, metadata)
            file_path = 'results/sweep' + '.' + ext
            file = open(file_path, 'w')
            for chunk in stream:
                file.write(chunk)
            print 'Sound exported to :' + file_path
            file.close()


class TestGraphers(Component):
    graphers = ExtensionPoint(timeside.graph.IGrapher)

    def list(self):
        graphers = []
        for grapher in self.graphers:
            graphers.append({'id':grapher.id(),
                            'name':grapher.name(),
                            })
        print graphers

    def run(self, media):
        print '\n=== Grapher testing ===\n'
        for grapher in self.graphers:
            id = grapher.id()
            image = grapher.render(media)
            file_path = 'results/'+id+'.png'
            file = open(file_path, 'w')
            for chunk in image:
                file.write(chunk)
            print 'Image exported to :' + file_path
            file.close()



if __name__ == '__main__':
    sample = 'samples/sweep.wav'
    metadata = {'creator': 'yomguy', 'date': '2009', 'name': 'test'}
    comp_mgr = ComponentManager()
    a = TestAnalyzers(comp_mgr)
    d = TestDecoders(comp_mgr)
    e = TestEncoders(comp_mgr)
    g = TestGraphers(comp_mgr)
    #a.list()
    #d.list()
    #e.list()
    #g.list()
    #a.run(sample)
    #g.run(sample)
    audio = d.run(sample, 'WAV')
    e.run(audio, metadata)


