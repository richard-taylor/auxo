
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.executor
import auxo.test.mocks
import unittest
        
class TestExecutor(unittest.TestCase):

    def testNoAgents(self):
        r = auxo.executor.run([])
        
        self.assertEqual(len(r), 0)
        
    def testGoodAgents(self):
        agents = [
            auxo.test.mocks.mockAgent("A", "hello"),
            auxo.test.mocks.mockAgent("B", "apple"),
            auxo.test.mocks.mockAgent("C", "orange")
        ]
        
        r = auxo.executor.run(agents)
        
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0].name, 'A')
        self.assertEqual(r[0].text, 'hello')
        self.assertEqual(r[1].name, 'B')
        self.assertEqual(r[1].text, 'apple')
        self.assertEqual(r[2].name, 'C')
        self.assertEqual(r[2].text, 'orange')
        
    def testBadAgents(self):
        agents = [
            auxo.test.mocks.mockAgent("A", None),
            auxo.test.mocks.mockAgent("B", "apple"),
            auxo.test.mocks.mockAgent("C", None)
        ]
        
        r = auxo.executor.run(agents)
        
        self.assertEqual(len(r), 3)
        self.assertEqual(r[0].name, 'A')
        self.assertEqual(r[0].text, 'Failed to complete.\n')
        self.assertEqual(r[1].name, 'B')
        self.assertEqual(r[1].text, 'apple')
        self.assertEqual(r[2].name, 'C')
        self.assertEqual(r[2].text, 'Failed to complete.\n')
        
