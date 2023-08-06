import AppKit
from PyObjCTools.TestSupport import TestCase, min_sdk_level
import objc


class TestNSPathCell(TestCase):
    def testConstants(self):
        self.assertEqual(AppKit.NSPathStyleStandard, 0)
        self.assertEqual(AppKit.NSPathStyleNavigationBar, 1)
        self.assertEqual(AppKit.NSPathStylePopUp, 2)

    def testMethods(self):
        m = AppKit.NSPathCell.setDoubleAction_.__metadata__()
        self.assertEqual(m["arguments"][2]["sel_of_type"], b"v@:@")

    @min_sdk_level("10.10")
    def testProtocols(self):
        objc.protocolNamed("NSPathCellDelegate")
