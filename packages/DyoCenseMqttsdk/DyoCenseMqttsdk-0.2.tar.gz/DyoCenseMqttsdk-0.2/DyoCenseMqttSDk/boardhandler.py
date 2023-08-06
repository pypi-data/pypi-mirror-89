"""Board Handler"""

class BoardHandler(object):
    '''methods for board related actions'''

    @classmethod
    def getserial(cls):
        '''get board serial number'''
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            _file = open('/proc/cpuinfo', 'r')
            for line in _file:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
            _file.close()
        except Exception:
            cpuserial = "00000000869abf9b"

        return cpuserial
