
import bs4
import logging

import auxo.agent
import auxo.report

url_base = 'http://wcadb.net/kinchranks.php'
url_query = url_base + '?region=United+Kingdom&gender=all&show=100'

class KinchAgent(auxo.agent.WebAgent):
	def __init__(self, name, url_param):
		super().__init__(name, url_query + '&kinch=' + url_param)
		
	def result(self):
		report = super().result()
		
		if self.content is None:
			report.addText('Failed to load the page.\n')
		else:
			try:
				soup = bs4.BeautifulSoup(self.content, 'html.parser')
				
				report.addText('OK parsed the HTML page.\n')
				
			except Exception as ex:
				logging.error('exception parsing HTML: ' + str(ex))
				report.addText('Failed to parse the HTML page.\n')
				
		return report
		
