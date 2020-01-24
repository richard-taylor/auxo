
import bs4
import hashlib

import auxo.agent
import auxo.report

url_whatson = 'https://www.yvonne-arnaud.co.uk/whats-on'
 
class YvonneArnaudAgent(auxo.agent.WebAgent):
    '''
    An agent which checks for new shows on at the Yvonne Arnaud theatre in Guildford.
    '''
    
    def __init__(self):
        super().__init__('Yvonne-Arnaud', url_whatson)
        
    def result(self):
        report = super().result()
        
        if 'shows' not in self.state:
            self.state['shows'] = {}
            
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            soup = bs4.BeautifulSoup(self.content, 'html.parser')
                
            # expecting something like:
            # <li>
            #   <a href="/production/the-silver-sword"> ... </a>      
            #   <div class="caption vevent">
            #     <h3 class="summary"><a href="/production/the-silver-sword">The Silver Sword</a></h3>
            #     <span class="date">2 Mar to 4 Mar</span>
    
            divs = soup.select('div.caption.vevent')
            
            # or
            # <li class="vevent">
            #   <h3 class="summary">Madama Butterfly (Encore Screening)</h3>
            #   <span class="date">2 Ap<li class="vevent">

            items = soup.select('li.vevent')

            new_shows = 0
            current_shows = {}
            
            for div in divs:
                date = div.select('span.date')[0].text.strip()
                title = div.select('h3.summary')[0].text.strip()
                
                new_shows += self.add_show(current_shows, date, title, report)
                
            for li in items:
                date = li.select('span.date')[0].text.strip()
                title = li.select('h3.summary')[0].text.strip()
                
                new_shows += self.add_show(current_shows, date, title, report)
            
            if new_shows > 0:
                report.addText('\nBook here: ' + self.url + '\n')
            
            # if there are no current shows then the website layout has
            # probably changed, so report that.
            if len(current_shows) > 0:
                self.state['shows'] = current_shows
            else:
                report.addText('No shows found. New format?\n')
            
        return report
        
    def add_show(self, shows, date, title, report):
        
        if (date == '') or (title == ''):
            return 0
                    
        show = { 'date': date, 'title': title }
            
        digest = hashlib.sha1()
        digest.update(date.encode('utf-8'))
        digest.update(title.encode('utf-8'))
                    
        show_id = digest.hexdigest()
                    
        shows[show_id] = show
                    
        if show_id not in self.state['shows']:
            report.addText('\n')
            report.addText('New show: ' + title + '\n')
            report.addText('    date: ' + date + '\n')
            return 1
            
        return 0 # not a new show

