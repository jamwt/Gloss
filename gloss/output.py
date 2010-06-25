import itertools
from gloss.colors import colors
import sys

job_count = itertools.count(1)
out = sys.stdout

class Task(object):
    def __init__(self, desc):
        self.desc = desc
        self.id = job_count.next()
        self.start()

    def start(self):
        print ' %s[%d] %s%s' % (colors.HEADER, self.id, self.desc, colors.ENDC)

    def subtask(self, msg):
        out.write('   %s ' % msg.ljust(60))
        out.flush()

    def st_okay(self):
        out.write('  %s[OK]%s\n' % (colors.OKGREEN, colors.ENDC))
        
    def st_fail(self, msg):
        msg = ' ' + msg.replace('\n', '\n ') + '\n\n'
        out.write('%s[FAIL]\n%s%s\n' % (colors.FAIL, msg, colors.ENDC))

    @classmethod
    def info(cls, msg, clear=True):
        msg = ' ' + colors.OKBLUE + msg.replace('\n', '\n ') + colors.ENDC + '\n\n'
        if not clear:
            msg = msg.rstrip() + '\n'
        out.write(msg)

    @classmethod
    def line(cls):
        print ""
