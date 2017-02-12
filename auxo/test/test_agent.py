
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.agent
import auxo.test.mocks
import os
import unittest

def helperRemove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass
        
class TestAgent(unittest.TestCase):

    def testBaseAgent(self):
        a = auxo.agent.BaseAgent('foo')
        self.assertEqual(a.name, 'foo')
        self.assertEqual(a.state['load-state-error'], 'loadState not called')
        
        helperRemove('/tmp/foo.json')
        a.loadState()
        self.assertEqual(a.state['load-state-error'], "[Errno 2] No such file or directory: '/tmp/foo.json'")
        a.saveState()
        a.loadState()
        self.assertEqual(a.state['load-state-error'], '')
        
        r = a.result()
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.text, None)
        
    def testWebAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHTTP(
            ({'status': '200', 'content-length': '4'}, b'1234'))
            
        a = auxo.agent.WebAgent('foo', 'http://example.com/')
        
        helperRemove('/tmp/foo.json')
        a.loadState()
        a.saveState()
        a.loadState()
        self.assertEqual(a.name, 'foo')
        self.assertEqual(a.url, 'http://example.com/')
        self.assertEqual(a.state['load-state-error'], '')
        
        r = a.result()
        self.assertEqual(a.state['http-status'], '200')
        self.assertEqual(a.state['content-length'], '4')
        self.assertEqual(a.content, b'1234')
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.text, None)
    
    def testHashWebAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHTTP(
            ({'status': '200', 'content-length': '5'}, b'12345'))
            
        a = auxo.agent.HashWebAgent('foo', 'http://example.com/')
        
        helperRemove('/tmp/foo.json')
        a.loadState()
        a.saveState()
        a.loadState()
        self.assertEqual(a.name, 'foo')
        self.assertEqual(a.url, 'http://example.com/')
        self.assertEqual(a.state['load-state-error'], '')
        
        r = a.result()
        self.assertEqual(a.state['http-status'], '200')
        self.assertEqual(a.state['content-length'], '5')
        self.assertEqual(a.state['content-hash'], '8cb2237d0679ca88db6464eac60da96345513964')
        self.assertEqual(a.content, b'12345')
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.text, 'The page has changed: http://example.com/\n')

