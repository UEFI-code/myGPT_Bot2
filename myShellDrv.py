import os
import pty
import select
import fcntl
import re
import time

class myShell():
    def __init__(self, maxChars = 512, monitor = None):
        self.maxChars = maxChars
        self.monitor = open(monitor, 'wb', buffering=0) if monitor != None else None
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
        delta = b''
        while True:
            r, _, _ = select.select([self.fd], [], [], 1.0)
            if r:
                try:
                    delta += os.read(self.fd, 2048)
                except:
                    continue
            else:
                # No data
                break
        self.ptyData += delta
        
        if self.monitor != None:
            self.monitor.write(delta)
        
        decoded_delta = delta.decode('utf-8').replace('\r', '')
        return decoded_delta[-self.maxChars:]
    
    def sendCmd(self, cmd):
        cmd += '\n'
        os.write(self.fd, cmd.encode('utf-8'))
        time.sleep(0.1)
        os.read(self.fd, len(cmd.encode('utf-8')))
    
    def translateScreen(self):
        translated = self.ansi_escape.sub('', self.ptyData.decode('utf-8')).replace('\r', '')
        translated = translated[-self.maxChars:]
        return translated.replace('\n', '<br>')

if __name__ == '__main__':
    myShellObj = myShell()
    myShellObj.getScreen()
    print(myShellObj.ptyData.decode('utf-8'))
    myShellObj.sendCmd('ifconfig')
    print(myShellObj.getScreen())
    print(myShellObj.translateScreen())
