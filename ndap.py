#!/usr/bin/python

from cnfmanager import CnfManager
from msgmanager import MsgManager
from filemanager import FileManager
from ndsscom import NdssCom
from netmanager import NetManager
import ndutil

from twisted.internet import reactor
from twisted.internet.protocol import Protocol,Factory


def ndap_loop():
    ndutil.set_timezone()

    cnfManager = CnfManager()
    cnfManager.load('./ndap.cnf')
    cnfData = cnfManager.get_cnf_data()

    msgManager = MsgManager()
    ndssCom = NdssCom('127.0.0.1', 12330)

    netManager = NetManager()
    netManager.set_msgmanager(msgManager)
    netManager.set_ndsscom(ndssCom)
    netManager.set_authcode(cnfData['authCode'])

    factory = Factory()
    factory.protocol = FileManager

    reactor.listenUDP(cnfData['comPort'], netManager)
    reactor.listenTCP(cnfData['filePort'], factory)
    reactor.run()

if __name__ == '__main__':
    ndap_loop()

