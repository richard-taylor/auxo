
import bs4
import logging

import auxo.agent
import auxo.report

url_base = 'http://wcadb.net/kinchranks.php'
url_query = url_base + '?region=United+Kingdom&gender=all&show=100'

class KinchAgent(auxo.agent.WebAgent):
    def __init__(self, agent_name, person, kinch):
        super().__init__(agent_name, url_query + '&kinch=' + kinch)
        
        self.person = person
        
    def result(self):
        report = super().result()
        
        if self.content is None:
            report.addText('Failed to load the page.\n')
        else:
            try:
                soup = bs4.BeautifulSoup(self.content, 'html.parser')
                
                # expecting something like:
                # <tr>
                #   <td>50</td>
                #   <td><a href="url">Person Name</a></td>
                #   <td>88.5</td>
                
                anchor = soup.find('a', href=True, text=self.person)
                
                if anchor is None:
                    report.addText('Cannot find ' + self.person + ' on the page.\n')
                    return report

                tr = anchor.parent.parent
                td = tr.find_all('td')
                
                rank = td[0].text
                score = td[2].text

                if (rank is None) or (rank == ''):
                    # probably a tie. TODO extract it from the previous row.
                    rank = '???'
                    
                if (score is None) or score == '':
                    report.addText('Cannot find the score on the page. New format?\n')
                    return report
                                            
                if ('rank' not in self.state) or (self.state['rank'] != rank):
                    report.addText('New rank: ' + rank + '\n')
                    self.state['rank'] = rank
                    
                if ('score' not in self.state) or (self.state['score'] != score):
                    report.addText('New score: ' + score + '\n')
                    self.state['score'] = score
                
            except IOError as ex:
                logging.error('Error parsing HTML: ' + str(ex))
                report.addText('Failed to parse the HTML page.\n')
                
        return report
        
