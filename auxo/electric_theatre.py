
import bs4
import hashlib
import re

import auxo.agent
import auxo.report

url_whatson = 'https://electric.theatre/events/'
 
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
                
            # Events just have a div like:
            #   <div class="event-dates">
            #     <h2 class="show-title">See How They Run</h2>
            #     <div class="event-date-range">18-19 October 2017</div>
    
            divs = soup.select('div.event-dates')
            
            new_events = 0
            current_events = {}
            
            for div in divs:
                h2 = div.select('h2.show-title')
                title = h2[0].text.strip()

                d2 = div.select('div.event-date-range')
                date = d2[0].text.strip()

                if title == '' or date == '':
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

