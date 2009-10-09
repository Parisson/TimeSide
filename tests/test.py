#!/usr/bin/python
# -*- coding: utf-8 -*-

import timeside
from timeside.core import Component, ExtensionPoint, ComponentManager

class TestAnalyzers(Component):
    analyzers = ExtensionPoint(timeside.analyze.IAnalyzer)

    def run(self):
        analyzers = []
        for analyzer in self.analyzers:
            analyzers.append({'name':analyzer.name(),
                            'id':analyzer.id(),
                            'unit':analyzer.unit(),
                            })
        print analyzers

class TestDecoders(Component):
    decoders = ExtensionPoint(timeside.decode.IDecoder)

    def run(self):
        decoders = []
        for decoder in self.decoders:
            decoders.append({'format':decoder.format(),
                            'mime_type':decoder.mime_type(),
                            })
        print decoders


class TestEncoders(Component):
    encoders = ExtensionPoint(timeside.encode.IEncoder)

    def run(self):
        encoders = []
        for encoder in self.encoders:
            encoders.append({'format':encoder.format(),
                            'mime_type':encoder.mime_type(),
                            })
        print encoders

class TestGraphers(Component):
    graphers = ExtensionPoint(timeside.graph.IGrapher)

    def run(self):
        graphers = []
        for grapher in self.graphers:
            graphers.append({'id':grapher.id(),
                            'name':grapher.name(),
                            })
        print graphers

if __name__ == '__main__':
    comp_mgr = ComponentManager()
    a = TestAnalyzers(comp_mgr)
    d = TestDecoders(comp_mgr)
    e = TestEncoders(comp_mgr)
    g = TestGraphers(comp_mgr)
    a.run()
    d.run()
    e.run()
    g.run()

