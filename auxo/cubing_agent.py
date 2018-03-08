
import bs4
import hashlib

import auxo.agent
import auxo.report

url_uk = 'https://www.worldcubeassociation.org/competitions?region=United+Kingdom'
 
class CubingAgent(auxo.agent.WebAgent):
    '''
    An agent which checks for new Rubik's Cube competitions on the World Cubing
    Association website.
    '''
    
    def __init__(self):
        super().__init__('Cubing', url_uk)
        
    def result(self):
        report = super().result()
        
        if 'comps' not in self.state:
            self.state['comps'] = {}
            
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            soup = bs4.BeautifulSoup(self.content, 'html.parser')
                
            # expecting something like:
            # <li class="list-group-item not-past">
            #   <span class="date">Apr 23 - 24, 2016</span>
            #   <span class="competition-info">
            #     <div class="competition-link">Bosnia and Herzegovina Open 2016</p>
            #     <div class="location">Bosnia and Herzegovina, Banja Luka</p>
        
            items = soup.select('li.list-group-item.not-past')
            
            new_comps = 0
            current_comps = {}
            
            for li in items:
                date = li.select('span.date')[0].text.strip()
                title = li.select('div.competition-link')[0].text.strip()
                location = li.select('div.location')[0].text.strip()
                
                if (date == '') or (title == '') or (location == ''):
                    continue
                    
                comp = { 'date': date, 'title': title, 'location': location }
            
                digest = hashlib.sha1()
                digest.update(date.encode('utf-8'))
                digest.update(title.encode('utf-8'))
                digest.update(location.encode('utf-8'))
                    
                comp_id = digest.hexdigest()
                    
                current_comps[comp_id] = comp
                    
                if comp_id not in self.state['comps']:
                    report.addText('\n')
                    report.addText('New competion: ' + title + '\n')
                    report.addText('     Location: ' + location + '\n')
                    report.addText('         Date: ' + date + '\n')
                    new_comps += 1
            
            if new_comps > 0:
                report.addText('\nRegister here: ' + self.url + '\n')
            
            # if there are no current competitions then the website layout has
            # probably changed, so report that.
            if len(current_comps) > 0:
                self.state['comps'] = current_comps
            else:
                report.addText('No competitions found. New format?\n')
            
        return report

