
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.electric_theatre
import auxo.test.mocks
import unittest
        
class TestElectricTheatreAgent(unittest.TestCase):

    def testElectricTheatreAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('electric-theatre.html')
        
        a = auxo.electric_theatre.ElectricTheatreAgent()
        r = a.result()
            
        events = a.state['events']
        self.assertEqual(len(events), 35)
            
        found = False
            
        for key, value in events.items():
            if value['title'] == "Disney's Aladdin Jr.":
                found = True
                self.assertEqual(value['date'], 'Thu 6 - Sat 8 Apr')
            
        self.assertTrue(found)

