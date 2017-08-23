
import auxo.report

class mockAgent(object):
    def __init__(self, name, text):
        self.name = name
        self.text = text
        
    def loadState(self):
        pass
    
    def saveState(self):
        pass
        
    def result(self):
        if self.text:
            return auxo.report.Report(self.name, self.text)
        else:
            raise Exception('no report')
        
class mockHTTP(object):
    def __init__(self, return_value):
        self.return_value = return_value
        
    def request(self, url, method, **keywords):
        return self.return_value

class mockHttpFile(mockHTTP):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            content = f.read()
            length = str(len(content))
            super().__init__(({'status': '200', 'content-length': length}, content))      
