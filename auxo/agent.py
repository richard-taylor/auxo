
import hashlib
import httplib2
import json
import logging
import os.path

import auxo.report

state_dir = '/tmp'

class BaseAgent(object):
    def __init__(self, name):
        self.name = name
        self.state = { 'load-state-error': 'loadState not called' }
        
    def loadState(self):
        self.filename = os.path.join(state_dir, self.name + '.json')
        try:
            with open(self.filename, 'r') as file:
                self.state = json.load(file)
            self.state['load-state-error'] = ''
        except (IOError, ValueError) as ex:
            logging.error('agent ' + self.name + ' exception loading state: ' + str(ex))
            self.state['load-state-error'] = str(ex)
        
    def saveState(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.state, file, indent=4)
        except IOError as ex:
            logging.error('agent ' + self.name + ' exception saving state: ' + str(ex))
        
    def result(self):
        return auxo.report.Report(self.name)

http = httplib2.Http('.html-cache')
        
class WebAgent(BaseAgent):
    def __init__(self, name, url):
        super().__init__(name)
        self.url = url
        
    def result(self):
        logging.info('Loading ' + self.url)
        
        (response, content) = http.request(self.url, 'GET')
        self.state['http-status'] = response['status']
        if response['status'] == '200':
            if 'content-length' in response:
                self.state['content-length'] = response['content-length']
            self.content = content
        else:
            self.content = None
            
        return super().result()
         
class HashWebAgent(WebAgent):
    def __init__(self, name, url):
        super().__init__(name, url)
        
    def result(self):
        report = super().result()
        
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            digest = hashlib.sha1()
            digest.update(self.content)
            hexdigest = digest.hexdigest()
            
            if ('content-hash' not in self.state) or \
               (self.state['content-hash'] != hexdigest):
                report.addText('The page has changed: ' + self.url + '\n')
            
            self.state['content-hash'] = hexdigest
                
        return report

