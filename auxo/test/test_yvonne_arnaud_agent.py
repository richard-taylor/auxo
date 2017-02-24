
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.yvonne_arnaud
import auxo.test.mocks
import unittest
        
class TestYvonneArnaudAgent(unittest.TestCase):

    def testYvonneArnaudAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('yvonne-arnaud.html')
        
        a = auxo.yvonne_arnaud.YvonneArnaudAgent()
        r = a.result()
            
        shows = a.state['shows']
        self.assertEqual(len(shows), 40)
            
        # look for one show currently running and one coming soon
        foundTSS = False
        foundOMIH = False
            
        for key, value in shows.items():

            if value['title'] == 'The Silver Sword':
                foundTSS = True
                self.assertEqual(value['date'], '2 Mar to 4 Mar')
                
            if value['title'] == 'Our Man in Havana':
                foundOMIH = True
                self.assertEqual(value['date'], '25 Apr to 29 Apr')
                
        self.assertTrue(foundTSS)
        self.assertTrue(foundOMIH)


