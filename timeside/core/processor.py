# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2013 Parisson SARL
# Copyright (c) 2009 Olivier Guilyardi <olivier@samalyse.com>
#
# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .component import Component, MetaComponent, abstract
from .component import implements, implementations, interfacedoc
from .api import IProcessor
from .exceptions import Error, PIDError, ApiError
from .tools.parameters import HasParam

import re
import numpy
import uuid
import networkx as nx
import inspect
import os


__all__ = ['Processor', 'MetaProcessor', 'implements', 'abstract',
           'interfacedoc', 'processors', 'get_processor', 'ProcessPipe',
           'FixedSizeInputAdapter']

_processors = {}


class MetaProcessor(MetaComponent):
    """Metaclass of the Processor class, used mainly for ensuring
    that processor id's are wellformed and unique"""

    valid_id = re.compile("^[a-z][_a-z0-9]*$")

    def __new__(cls, name, bases, d):
        new_class = super(MetaProcessor, cls).__new__(cls, name, bases, d)
        if new_class in implementations(IProcessor):
            id = str(new_class.id())
            if id in _processors:
                # Doctest test can duplicate a processor
                # This can be identify by the conditon "module == '__main__'"
                new_path = os.path.realpath(inspect.getfile(new_class))
                id_path = os.path.realpath(inspect.getfile(_processors[id]))
                if new_class.__module__ == '__main__':
                    new_class = _processors[id]
                elif _processors[id].__module__ == '__main__':
                    pass
                elif new_path == id_path:
                    new_class = _processors[id]
                else:
                    raise ApiError("%s at %s and %s at %s have the same id: '%s'"
                                   % (new_class.__name__, new_path,
                                      _processors[id].__name__, id_path,
                                      id))
            if not MetaProcessor.valid_id.match(id):
                raise ApiError("%s has a malformed id: '%s'"
                               % (new_class.__name__, id))

            _processors[id] = new_class

        return new_class


class Processor(Component, HasParam):

    """Base component class of all processors


    Attributes:
              parents :  Dictionnary of parent Processors that must be
                         processed before the current Processor
              pipe :     The ProcessPipe in which the Processor will run
        """
    __metaclass__ = MetaProcessor

    abstract()
    implements(IProcessor)

    type = ''

    def __init__(self):
        super(Processor, self).__init__()

        self.parents = {}
        self._parameters = {}
        self.source_mediainfo = None
        self.process_pipe = None
        self._uuid = uuid.uuid4()

        self.input_channels = 0
        self.input_samplerate = 0
        self.input_blocksize = 0
        self.input_stepsize = 0

    @interfacedoc
    def setup(self, channels=None, samplerate=None, blocksize=None,
              totalframes=None):
        self.source_channels = channels
        self.source_samplerate = samplerate
        self.source_blocksize = blocksize
        self.source_totalframes = totalframes

        # If empty Set default values for input_* attributes
        # may be setted by the processor during __init__()
        if not self.input_channels:
            self.input_channels = self.source_channels
        if not self.input_samplerate:
            self.input_samplerate = self.source_samplerate
        if not self.input_blocksize:
            self.input_blocksize = self.source_blocksize
        if not self.input_stepsize:
            self.input_stepsize = self.input_blocksize

        # Check samplerate specification if any
        if self.force_samplerate:
            if self.input_samplerate != self.force_samplerate:
                raise ValueError(
                    '%s requires %d input sample rate: %d provided' %
                    (self.__class__.__name__, self.force_samplerate,
                     self.input_samplerate))

    # default channels(), samplerate() and blocksize() implementations returns
    # the source characteristics, but processors may change this behaviour by
    # overloading those methods
    @interfacedoc
    def channels(self):
        return self.source_channels

    @interfacedoc
    def samplerate(self):
        return self.source_samplerate

    @interfacedoc
    def blocksize(self):
        return self.source_blocksize

    @interfacedoc
    def totalframes(self):
        return self.source_totalframes

    @interfacedoc
    def process(self, frames, eod):
        return frames, eod

    @interfacedoc
    def post_process(self):
        pass

    @interfacedoc
    def release(self):
        pass

    @interfacedoc
    def mediainfo(self):
        return self.source_mediainfo

    @interfacedoc
    def uuid(self):
        return str(self._uuid)

    @interfacedoc
    @classmethod
    def description(self):
        try:
            descr = self.__doc__.lstrip().split('\n')[0]
        except AttributeError:
            return '*** NO DESCRIPTION FOR THIS PROCESSOR ***'

        return descr

    @property
    def force_samplerate(self):
        return None

    def __del__(self):
        self.release()

    def __or__(self, other):
        return ProcessPipe(self, other)

    def __eq__(self, other):
        return (self.id() == other.id() and
                self.get_parameters() == other.get_parameters())

    def __repr__(self):
        return '-'.join([self.id(), self.get_parameters().__repr__()])


class FixedSizeInputAdapter(object):

    """Utility to make it easier to write processors which require fixed-sized
    input buffers."""

    def __init__(self, buffer_size, channels, pad=False):
        """Construct a new adapter:
        buffer_size is the desired buffer size in frames,
        channels the number of channels, and pad indicates whether the last
        block should be padded with zeros."""

        self.buffer = numpy.empty((buffer_size, channels))
        self.buffer_size = buffer_size
        self.len = 0
        self.pad = pad

    def blocksize(self, input_totalframes):
        """Return the total number of frames that this adapter will output
        according to the input_totalframes argument"""

        blocksize = input_totalframes
        if self.pad:
            mod = input_totalframes % self.buffer_size
            if mod:
                blocksize += self.buffer_size - mod

        return blocksize

    def process(self, frames, eod):
        """Returns an iterator over tuples of the form (buffer, eod)
        where buffer is a fixed-sized block of data, and eod indicates whether
        this is the last block.
        In case padding is deactivated the last block may be smaller than
        the buffer size.
        """
        src_index = 0
        remaining = len(frames)

        while remaining:
            space = self.buffer_size - self.len
            copylen = remaining < space and remaining or space
            src = frames[src_index:src_index + copylen]
            if self.len == 0 and copylen == self.buffer_size:
                # avoid unnecessary copy
                buffer = src
            else:
                buffer = self.buffer
                buffer[self.len:self.len + copylen] = src

            remaining -= copylen
            src_index += copylen
            self.len += copylen

            if self.len == self.buffer_size:
                yield buffer, (eod and not remaining)
                self.len = 0

        if eod and self.len:
            block = self.buffer
            if self.pad:
                self.buffer[self.len:self.buffer_size] = 0
            else:
                block = self.buffer[0:self.len]

            yield block, True
            self.len = 0


def processors(interface=IProcessor, recurse=True):
    """Returns the processors implementing a given interface and, if recurse,
    any of the descendants of this interface."""
    return implementations(interface, recurse)


def get_processor(processor_id):
    """Return a processor by its id"""
    if not processor_id in _processors:
        raise PIDError("No processor registered with id: '%s'"
                       % processor_id)

    return _processors[processor_id]


def list_processors(interface=IProcessor, prefix=""):
    print prefix + interface.__name__
    if len(prefix):
        underline_char = '-'
    else:
        underline_char = '='
    print prefix + underline_char * len(interface.__name__)
    subinterfaces = interface.__subclasses__()
    for i in subinterfaces:
        list_processors(interface=i, prefix=prefix + "  ")
    procs = processors(interface, False)
    for p in procs:
        print prefix + "  * %s :" % p.id()
        print prefix + "    \t\t%s" % p.description()


def list_processors_rst(interface=IProcessor, prefix=""):
    print '\n' + interface.__name__
    if len(prefix):
        underline_char = '-'
    else:
        underline_char = '='
    print underline_char * len(interface.__name__) + '\n'
    subinterfaces = interface.__subclasses__()
    for i in subinterfaces:
        list_processors_rst(interface=i, prefix=prefix + " ")
    procs = processors(interface, False)
    for p in procs:
        print prefix + "  * **%s** : %s" % (p.id(), p.description())


class ProcessPipe(object):

    """Handle a pipe of processors
    Attributes:
        processor: List of all processors in the Process pipe
        results : Dictionnary of Results Container from all the analyzers
                  in the Pipe process
    """

    def __init__(self, *others):
        self.processors = []
        self._streamer = None
        self._stream_thread = False
        self._is_running = False
        self._graph = nx.DiGraph(name='ProcessPipe')

        self |= others

        self.results = {}

    def append_processor(self, proc, source_proc=None):
        "Append a new processor to the pipe"
        if source_proc is None and len(self.processors):
            source_proc = self.processors[0]

        if source_proc and not isinstance(source_proc, Processor):
            raise TypeError('source_proc must be a Processor or None')

        if not isinstance(proc, Processor):
            raise TypeError('proc must be a Processor or None')

        if proc.type == 'decoder' and len(self.processors):
            raise ValueError('Only the first processor in a pipe could be a Decoder')

        # TODO : check if the processor is already in the pipe
        if source_proc:
            for child in self._graph.neighbors_iter(source_proc.uuid()):
                child_proc = self._graph.node[child]['processor']
                if proc == child_proc:
                    proc._uuid = child_proc.uuid()
                    proc.process_pipe = self
                    break
        if not self._graph.has_node(proc.uuid()):
            self.processors.append(proc)  # Add processor to the pipe
            self._graph.add_node(proc.uuid(), processor=proc, id=proc.id())
            if source_proc:
                self._graph.add_edge(self.processors[0].uuid(), proc.uuid(),
                                     type='audio_source')
            proc.process_pipe = self
            # Add an edge between each parent and proc
            for parent in proc.parents.values():
                self._graph.add_edge(parent.uuid(), proc.uuid(),
                                     type='data_source')

    def append_pipe(self, proc_pipe):
        "Append a sub-pipe to the pipe"

        for proc in proc_pipe.processors:
            self.append_processor(proc)

    def draw_graph(self):
        import matplotlib.pyplot as plt

        elarge = [(u, v) for (u, v, d) in self._graph.edges(data=True)
                  if d['type'] == 'audio_source']
        esmall = [(u, v) for (u, v, d) in self._graph.edges(data=True)
                  if d['type'] == 'data_source']

        pos = nx.shell_layout(self._graph)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(self._graph, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(self._graph, pos, edgelist=elarge,
                               arrows=True)
        nx.draw_networkx_edges(self._graph, pos, edgelist=esmall,
                               alpha=0.5, edge_color='b',
                               style='dashed', arrows=True)

        # labels
        labels = {node: repr(self._graph.node[node]['processor']) for node in self._graph.nodes()}
        nx.draw_networkx_labels(self._graph, pos, labels, font_size=20,
                                font_family='sans-serif')

        plt.axis('off')
        plt.show()  # display

    def __or__(self, other):
        self |= other
        return self

    def __ior__(self, other):
        if isinstance(other, Processor):
            for parent in other.parents.values():
                self |= parent
            self.append_processor(other)

        elif isinstance(other, ProcessPipe):
            self.append_pipe(other)
        else:
            try:
                iter(other)
            except TypeError:
                raise Error("Can not add this type of object to a pipe: %s",
                            str(other))

            for item in other:
                self |= item

        return self

    def __repr__(self):
        pipe = ''
        for item in self.processors:
            pipe += item.id()
            if item != self.processors[-1]:
                pipe += ' | '
        return pipe

    def run(self, channels=None, samplerate=None, blocksize=None):
        """Setup/reset all processors in cascade"""

        source = self.processors[0]
        items = self.processors[1:]

        # Check if any processor in items need to force the samplerate
        force_samplerate = set([item.force_samplerate for item in items
                                if item.force_samplerate])
        if force_samplerate:
            if len(force_samplerate) > 1:
                raise(ValueError,
                      "Some processors specify different samplerate")
            force_samplerate = force_samplerate.pop()

            if samplerate and samplerate != force_samplerate:
                raise(ValueError, "A processor try to force the samplerate")

            samplerate = force_samplerate

        source.setup(channels=channels, samplerate=samplerate,
                     blocksize=blocksize)
        source.SIG_STOP = False
        last = source

        # setup/reset processors and configure properties throughout the pipe
        for item in items:
            item.source_mediainfo = source.mediainfo()
            item.setup(channels=last.channels(),
                       samplerate=last.samplerate(),
                       blocksize=last.blocksize(),
                       totalframes=last.totalframes())
            self._register_streamer(item)
            last = item

        # now stream audio data along the pipe
        if self._stream_thread:
            self._running_cond.acquire()
        self._is_running = True
        if self._stream_thread:
            self._running_cond.notify()
            self._running_cond.release()

        eod = False

        if source.id() == 'live_decoder':
            # Set handler for Interruption signal
            import signal

            def signal_handler(signum, frame):
                source.stop()

            signal.signal(signal.SIGINT, signal_handler)

        while not eod:
            frames, eod = source.process()
            for item in items:
                frames, eod = item.process(frames, eod)

        if source.id() == 'live_decoder':
            # Restore default handler for Interruption signal
            signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Post-processing
        for item in items:
            item.post_process()

        # Release source
        source.release()
        # Release processors
        for item in items:
            item.release()

        self._is_running = False

    def stream(self):
        self._stream_thread = True

        import threading

        class PipeThread(threading.Thread):

            def __init__(self, process_pipe):
                super(PipeThread, self).__init__(name='pipe_thread')
                self.process_pipe = process_pipe

            def run(self):
                self.process_pipe.run()

        pipe_thread = PipeThread(self)
        pipe_thread.start()

        # wait for pipe thread to be ready to stream
        self._running_cond = threading.Condition(threading.Lock())
        self._running_cond.acquire()
        while not self._is_running:
            self._running_cond.wait()
        self._running_cond.release()

        if self._streamer is None:
            raise TypeError('Function only available in streaming mode')

        while pipe_thread.is_alive():
            # yield count
            chunk = self._streamer.get_stream_chunk()
            if chunk is not None:
                yield chunk
            else:
                break

    def _register_streamer(self, processor):
        if hasattr(processor, 'streaming') and processor.streaming:
            if self._streamer is None:
                self._streamer = processor
            else:
                raise TypeError('More than one streaming processor in pipe')
