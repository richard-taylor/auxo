
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.electric_theatre
import auxo.test.mocks
import unittest
        
class TestElectricTheatreAgent(unittest.TestCase):

    def testElectricTheatreAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('electric-theatre-2.html')
        
        a = auxo.electric_theatre.ElectricTheatreAgent()
        r = a.result()
            
        events = a.state['events']
        self.assertEqual(len(events), 21)
            
        found = False
            
        for key, value in events.items():
            if value['title'] == "You Are Not Alone":
                found = True
                self.assertEqual(value['date'], 'Thursday 28 September 2017')
            
        self.assertTrue(found)

