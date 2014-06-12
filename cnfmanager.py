#!/usr/bin/python

import ConfigParser
import os

class CnfManager():
    def load(self, cnfFile):
        if not os.path.isfile(cnfFile):
            cnfFile = './ndap.cnf'

        cf = ConfigParser.ConfigParser()
        cf.read(cnfFile)

        self.cnfData = {}
        self.cnfData['comPort'] = int(cf.get('com', 'comPort'))
        self.cnfData['filePort'] = int(cf.get('com', 'filePort'))
        self.cnfData['authCode'] = cf.get('auth', 'authCode')

    def get_cnf_data(self):
        return self.cnfData
