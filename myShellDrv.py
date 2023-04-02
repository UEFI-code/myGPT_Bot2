import os
import pty
import select
import fcntl
import re

class myShell():
    def __init__(self, maxChars = 512):
        self.maxChars = maxChars
        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        self.ptyData = b''
        self.os = os.name
        pid, self.fd = pty.fork()
        if pid == 0:
            # Child
            if self.os == 'nt':
                os.execlp('cmd', 'cmd')
            else:
                os.execlp('bash', 'bash')
        else:
            flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    def getScreen(self):
        while True:
            r, _, _ = select.select([self.fd], [], [], 1.0)
            if r:
                try:
                    self.ptyData += os.read(self.fd, 1024)
                except:
                    continue
            else:
                # No data
                break
    
    def sendCmd(self, cmd):
        cmd += '\n'
        os.write(self.fd, cmd.encode('utf-8'))
    
    def translateScreen(self):
        translated = self.ansi_escape.sub('', self.ptyData.decode('utf-8')).replace('\r', '')
        if(len(translated) > self.maxChars):
            translated = translated[len(translated) - self.maxChars:]
        return translated.replace('\n', '<br>')

if __name__ == '__main__':
    myShellObj = myShell()
    myShellObj.getScreen()
    print(myShellObj.ptyData.decode('utf-8'))
    myShellObj.sendCmd('ifconfig')
    myShellObj.getScreen()
    print(myShellObj.translateScreen())
