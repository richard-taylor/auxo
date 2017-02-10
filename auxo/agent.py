
import hashlib
import httplib2
import json
import logging
import os.path
import re

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

class GLiveAgent(WebAgent):
    def __init__(self):
        super().__init__('GLive', 'https://glive.co.uk/Online/allevents')
        
        self.re_event = re.compile(r'\s*\[ ("[^"]*", ){26}(\[[^\]]*\], ){2}("[^"]*", ){35}("[^"]*"){1} \]')
        self.re_array = re.compile(r'\[[^\[\]]*\]')
        self.re_quote = re.compile(r'"[^"]*"')
        
        if 'events' not in self.state:
            self.state['events'] = {}
        
    def result(self):
        report = super().result()
        
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            content_string = self.content.decode('utf-8')
            more_events = False
            current_events = {}
            
            for line in content_string.split('\n'):
                if self.re_event.match(line):
                    noarray = self.re_array.sub('""', line)
                    quotes = self.re_quote.findall(noarray)
                    
                    event = {
                            'description': quotes[5].strip('"'),
                            'start date': quotes[7].strip('"'),
                            'end date': quotes[8].strip('"'),
                            'min price': quotes[59].strip('"'),
                            'max price': quotes[60].strip('"')
                            }
                    
                    event_id = quotes[0].strip('"')
                    
                    current_events[event_id] = event
                    
                    if event_id in self.state['events']:
                        previous = self.state['events'][event_id]
                        if previous['description'] != event['description'] \
                        or previous['start date'] != event['start date'] \
                        or previous['end date'] != event['end date'] \
                        or previous['min price'] != event['min price'] \
                        or previous['max price'] != event['max price']:
                            report.addText('\nChanged event: ' + event['description'] + '\n')
                            report.addText('From:          ' + event['start date'] + '\n')
                            report.addText('Until:         ' + event['end date'] + '\n')
                            report.addText('Prices:        ' + event['min price'] + ' - ' + event['max price'] + '\n')
                            more_events = True
                    else:
                        report.addText('\n**New** event: ' + event['description'] + '\n')
                        report.addText('From:          ' + event['start date'] + '\n')
                        report.addText('Until:         ' + event['end date'] + '\n')
                        report.addText('Prices:        ' + event['min price'] + ' - ' + event['max price'] + '\n')
                        more_events = True
            
            if more_events:
                report.addText('\nbook here: ' + self.url + '\n')
            
            # if there are no current events then the website layout has
            # probably changed, so report that.
            if len(current_events) > 0:
                self.state['events'] = current_events
            else:
                report.addText('No events found. Format has changed?\n')
            
        return report
