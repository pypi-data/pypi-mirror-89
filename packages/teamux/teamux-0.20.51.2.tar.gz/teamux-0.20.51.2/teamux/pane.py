from re import search
from time import sleep
from types import SimpleNamespace as ns

from .base import Base


class Pane(Base):
    keys = '''
        session_id
        window_id
        pane_id
        pane_active
        pane_index
        pane_width
        pane_height
        pane_title
        pane_pid
        pane_start_command
        pane_start_path
        pane_current_path
        pane_current_command
    '''

    def __init__(self, window, fields):
        self.window = window
        self.fields = fields

    def send(self, keys):
        self.tmux('send-keys', keys)
        self.tmux('send-keys', 'Enter')

    def send_keys(self, keys):
        self.tmux('send-keys', keys)

    def script(self, source):
        for line in source.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                self.send(line)

    @property
    def capture(self):
        return self.tmux('capture-pane', '-p')

    def search(self, pat, line, num):
        found = search(pat, line)
        if found:
            grp = found.groupdict()
            grp['line'] = line
            grp['num'] = num
            return ns(**grp)

    def parse(self, pat, num=-1):
        line = self.capture[num]
        return self.search(pat, line, num)

    def find(self, pat):
        num = 0
        for line in reversed(self.capture):
            num-=1
            found = self.search(pat, line, num)
            if found:
                return found

    def find_all(self, pat):
        for num, line in enumerate(self.capture):
            found = self.search(pat, line, num)
            if found:
                yield found

    def wait(self, pat, msg=None):
        go = True
        while go:
            sleep(1)
            out = self.capture
            if not out: continue
            for line in out[-3:]:
                if search(pat, line):
                    go = False
        if msg:
            print(msg)

    def run(self, pane, cmd, exp=None, msg=None):
        self.send(cmd)
        if exp:
            self.wait(exp, msg)

    def __str__(self):
        return f"{self.is_active and '*' or ' '} {self.pane_title}{self.pane_id}"

