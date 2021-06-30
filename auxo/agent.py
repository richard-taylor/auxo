
import datetime
import hashlib
import httplib2
import json
import logging
import os.path
import re

import auxo.report

state_dir = '/tmp'
time_format = '%Y-%m-%dT%H:%M:%S'

class BaseAgent(object):
    '''
    Base class for agents with a small amount of state information.
    
    State is saved as a JSON object, with the same name as the agent, in the
    auxo.agent.state_dir directory.
    '''
    
    def __init__(self, name):
        self.name = name
        self.state = { 'load-state-error': 'loadState not called' }
        self.filename = os.path.join(state_dir, self.name + '.json')
        
    def loadState(self):
        try:
            with open(self.filename, 'r') as file:
                self.state = json.load(file)
            self.state['load-state-error'] = ''
        except (IOError, ValueError) as ex:
            logging.error('agent ' + self.name + ' exception loading state: ' + str(ex))
            self.state['load-state-error'] = str(ex)

        if 'last-changed' not in self.state:
            self.changed_now()

    def saveState(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.state, file, indent=4)
        except IOError as ex:
            logging.error('agent ' + self.name + ' exception saving state: ' + str(ex))
        
    def result(self):
        '''
        Perform the agent's operations, update the state and return a Report object.
        '''
        return auxo.report.Report(self.name)

    def changed_now(self):
        self.state['last-changed'] = datetime.datetime.now().strftime(time_format)

    def unchanged_days(self):
        now = datetime.datetime.now()
        then = datetime.datetime.strptime(self.state['last-changed'], time_format)
        return (now - then).days

http = httplib2.Http('.html-cache')
        
class WebAgent(BaseAgent):
    '''
    Base class for agents which load a web page.
    '''
    
    def __init__(self, name, url):
        super().__init__(name)
        self.url = url
        
    def result(self):
        logging.info('Loading ' + self.url)

        ua = {'User-Agent': 'auxo/2.2.2'}
        
        (response, content) = http.request(self.url, 'GET', headers = ua)
        self.state['http-status'] = response['status']
        if response['status'] == '200' or response['status'] == '304':
            if 'content-length' in response:
                self.state['content-length'] = response['content-length']
            self.content = content
        else:
            self.content = None
            
        return super().result()
         
class HashWebAgent(WebAgent):
    '''
    A simple web agent that loads a page and compares a hash of the content to
    the previous hash. So a simple way to check if a page has changed.
    '''
    
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
                self.changed_now()
            else:
                report.addText('Last changed ' + str(self.unchanged_days()) + ' days ago.\n')

            self.state['content-hash'] = hexdigest
                
        return report

class PatternWebAgent(WebAgent):
    '''
    A simple web agent that loads a page and looks for a regular expression
    pattern in the content. It can report either the presence or absence of
    the pattern.
    '''
    
    def __init__(self, name, url, pattern, present=None, absent=None):
        super().__init__(name, url)
        self.pattern = pattern
        self.present = present
        self.absent = absent
        
    def result(self):
        report = super().result()
        
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            search = re.search(self.pattern, self.content)
            
            if search is None and self.absent is not None:
                report.addText(self.absent + ' : ' + self.url + '\n')
            
            if search is not None and self.present is not None:
                report.addText(self.present + ' : ' + self.url + '\n')
                
        return report

