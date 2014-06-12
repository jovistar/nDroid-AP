from twisted.internet.protocol import DatagramProtocol
from ndsscom import NdssCom
from msgmanager import MsgManager
import ndutil

class NetManager(DatagramProtocol):
    def set_msgmanager(self, msgManager):
        self.msgManager = msgManager

    def set_ndsscom(self, ndssCom):
        self.ndssCom = ndssCom

    def set_authcode(self, authCode):
        self.authCode = authCode

    def datagramReceived(self, data, (host, port)):
        retCode, result = self.msgManager.res_request(data)
        if retCode != 0:
            pass
        else:
            authResult = self.auth_user(result)
            if authResult!= 0:
                return self.gen_response_error(authResult)

            responseData = None
            if result['request'] == 'scan':
                responseData = self.dispatch_scan(result)
            elif result['request'] == 'report':
                responseData = self.dispatch_report(result)

            msg = self.msgManager.gen_response(responseData)
            self.transport.write(msg, (host, port))

    def auth_user(self, data):
        if data.get('authCode') == None:
            return 1
        authCode = data['authCode']
        if authCode != self.authCode:
            return 3
        return 0

    def dispatch_scan(self, data):
        if data.get('uid') == None:
            return self.gen_response_error(1)

        uid = data['uid']

        responseData = {}
        retCode, result = self.ndssCom.scan_uid(uid)
        if retCode == 2:
            return self.gen_response_error(2)
        elif retCode == 1:
            return self.gen_response_error(1)
        elif retCode == 0:
            responseData['response'] = 0
            responseData['state'] = result
        return responseData

    def dispatch_report(self, data):
        return self.gen_response_error(1)

    def gen_response_error(self, retCode):
        responseData = {}
        responseData['response'] = retCode
        return responseData
