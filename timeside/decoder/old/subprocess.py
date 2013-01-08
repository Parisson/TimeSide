
class SubProcessPipe:

    def __init__(self, command, stdin=None):
        """Read media and stream data through a generator.
        Taken from Telemeta (see http://telemeta.org)"""

        self.buffer_size = 0xFFFF

        if not stdin:
            stdin = subprocess.PIPE

        self.proc = subprocess.Popen(command.encode('utf-8'),
                    shell = True,
                    bufsize = self.buffer_size,
                    stdin = stdin,
                    stdout = subprocess.PIPE,
                    close_fds = True)

        self.input = self.proc.stdin
        self.output = self.proc.stdout


class DecoderSubProcessCore(Processor):
    """Defines the main parts of the decoding tools :
    paths, metadata parsing, data streaming thru system command"""

    def __init__(self):
        self.command = 'ffmpeg -i "%s" -f wav - '

    def process(self, source, options=None):
        """Encode and stream audio data through a generator"""

        command = self.command % source
        proc = SubProcessPipe(command)
        return proc.output

        #while True:
            #__chunk = proc.output.read(self.proc.buffer_size)
            #status = proc.poll()
            #if status != None and status != 0:
                #raise ExportProcessError('Command failure:', command, proc)
            #if len(__chunk) == 0:
                #break
            #yield __chunk




