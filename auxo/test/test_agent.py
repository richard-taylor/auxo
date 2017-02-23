
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
        
    def testPatternWebAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHTTP(
            ({'status': '200', 'content-length': '22'}, b'An interesting message'))
            
        a1 = auxo.agent.PatternWebAgent('foo', 'http://example.com/', b'rest', present='yes')
        r1 = a1.result()
        self.assertEqual(r1.name, 'foo')
        self.assertEqual(r1.text, 'yes : http://example.com/\n')
        
        a2 = auxo.agent.PatternWebAgent('bar', 'http://example.com/', b'change', present='yes')
        r2 = a2.result()
        self.assertEqual(r2.name, 'bar')
        self.assertEqual(r2.text, None)
        
        a3 = auxo.agent.PatternWebAgent('foo', 'http://example.com/', b'change', absent='no')
        r3 = a3.result()
        self.assertEqual(r3.name, 'foo')
        self.assertEqual(r3.text, 'no : http://example.com/\n')
        
        a4 = auxo.agent.PatternWebAgent('bar', 'http://example.com/', b'rest', absent='no')
        r4 = a4.result()
        self.assertEqual(r4.name, 'bar')
        self.assertEqual(r4.text, None)
        
        a5 = auxo.agent.PatternWebAgent('f', 'http://x.co', b'r.s.', present='y', absent='n')
        r5 = a5.result()
        self.assertEqual(r5.name, 'f')
        self.assertEqual(r5.text, 'y : http://x.co\n')
        
        a6 = auxo.agent.PatternWebAgent('b', 'http://x.co', b't.t.', present='y', absent='n')
        r6 = a6.result()
        self.assertEqual(r6.name, 'b')
        self.assertEqual(r6.text, 'n : http://x.co\n')

