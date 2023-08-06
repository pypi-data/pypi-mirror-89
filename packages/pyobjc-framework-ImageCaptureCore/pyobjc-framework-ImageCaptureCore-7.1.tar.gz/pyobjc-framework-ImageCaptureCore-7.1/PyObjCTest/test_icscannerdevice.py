import ImageCaptureCore
from PyObjCTools.TestSupport import TestCase
import objc


class TestICScannerDevice(TestCase):
    def testConstants(self):
        self.assertIsInstance(ImageCaptureCore.ICScannerStatusWarmingUp, str)
        self.assertIsInstance(ImageCaptureCore.ICScannerStatusWarmUpDone, str)
        self.assertIsInstance(ImageCaptureCore.ICScannerStatusRequestsOverviewScan, str)

        self.assertEqual(ImageCaptureCore.ICScannerTransferModeFileBased, 0)
        self.assertEqual(ImageCaptureCore.ICScannerTransferModeMemoryBased, 1)

    def testProtocolObjects(self):
        objc.protocolNamed("ICScannerDeviceDelegate")
