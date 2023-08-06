import objc
import objc._objc
from objc._protocols import PROTOCOL_CACHE
from PyObjCTools.TestSupport import TestCase


class TestProtocols(TestCase):
    def testBasic(self):
        PROTOCOL_CACHE.clear()
        p = objc.protocolNamed("NSObject")
        self.assertIsInstance(p, objc.formal_protocol)

    def testNoProtocol(self):
        self.assertRaises(
            objc.ProtocolError, objc.protocolNamed, "PyObjCFooBarProtocol"
        )

    def testBasic2(self):
        orig_protocolsForProcess = objc._objc.protocolsForProcess
        try:
            objc._objc.protocolsForProcess = lambda: []
            PROTOCOL_CACHE.clear()

            p = objc.protocolNamed("NSObject")
            self.assertIsInstance(p, objc.formal_protocol)

        finally:
            objc._objc.protocolsForProcess = orig_protocolsForProcess
