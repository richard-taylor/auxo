
import bs4
import hashlib
import re

import auxo.agent
import auxo.report

url_whatson = 'http://www.guildford.gov.uk/electrictheatre/article/14768/Whats-on'
 
class ElectricTheatreAgent(auxo.agent.WebAgent):
    '''
    An agent which checks for new events on at the Electric Theatre
    in Guildford.
    '''
    
    def __init__(self):
        super().__init__('Electric-Theatre', url_whatson)
        
    def result(self):
        report = super().result()
        
        if 'events' not in self.state:
            self.state['events'] = {}
            
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            soup = bs4.BeautifulSoup(self.content, 'html.parser')
                
            # There is very little semantic structure on this site.
            # Events just have unclassed wrapping and a link like:
            #
            # <a href="link">The title <span>  Sat 14 Jun  </span></a>
    
            spans = soup.find_all('span')
            
            new_events = 0
            current_events = {}
            
            for span in spans:
                date = span.text.strip()

                if re.search('\S\S\S\s\d+\s\S\S\S', date) is None:
                    continue

                title = span.parent.contents[0].strip()
                
                if title == '':
                    continue
                    
                event = { 'date': date, 'title': title }
            
                digest = hashlib.sha1()
                digest.update(date.encode('utf-8'))
                digest.update(title.encode('utf-8'))
                    
                event_id = digest.hexdigest()
                    
                current_events[event_id] = event
                    
                if event_id not in self.state['events']:
                    report.addText('\n')
                    report.addText('New event: ' + title + '\n')
                    report.addText('     date: ' + date + '\n')
                    new_events += 1
            
            if new_events > 0:
                report.addText('\nBook here: ' + self.url + '\n')
            
            # if there are no current events then the website layout has
            # probably changed, so report that.
            if len(current_events) > 0:
                self.state['events'] = current_events
            else:
                report.addText('No events found. New format?\n')
            
        return report

