from ndsscom import NdssCom
import ndutil
import os

from twisted.internet.protocol import Protocol

class FileManager(Protocol):
    def connectionMade(self):
        ndutil.enable_dir('tmp')
        self.filePath = 'tmp/%s.apk' % ndutil.get_md5_by_str(ndutil.get_current_time)

        self.fileHandle = open(self.filePath, 'w')
        self.ndssCom = NdssCom('127.0.0.1', 12330)

    def connectionLost(self, reason):
        self.fileHandle.close()
        
        if not ndutil.is_apk_valid(self.filePath):
            os.remove(self.filePath)
        else:
            retCode, result = self.ndssCom.scan_file(self.filePath)
            if retCode != 0:
                os.remove(self.filePath)

    def dataReceived(self, data):
        self.fileHandle.write(data)
