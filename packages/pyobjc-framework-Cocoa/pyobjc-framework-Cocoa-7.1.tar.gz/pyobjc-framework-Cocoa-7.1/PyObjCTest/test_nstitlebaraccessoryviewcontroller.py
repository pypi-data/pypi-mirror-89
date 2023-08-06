import AppKit
from PyObjCTools.TestSupport import TestCase, min_os_level


class TestNSTitlebarAccessoryViewController(TestCase):
    @min_os_level("10.12")
    def test_methods10_12(self):
        self.assertResultIsBOOL(AppKit.NSTitlebarAccessoryViewController.isHidden)
        self.assertArgIsBOOL(AppKit.NSTitlebarAccessoryViewController.setHidden_, 0)

    @min_os_level("10.16")
    def test_methods10_16(self):
        self.assertResultIsBOOL(
            AppKit.NSTitlebarAccessoryViewController.automaticallyAdjustsSize
        )
        self.assertArgIsBOOL(
            AppKit.NSTitlebarAccessoryViewController.setAutomaticallyAdjustsSize_, 0
        )
