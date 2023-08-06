import Metal
import objc
from PyObjCTools.TestSupport import TestCase, min_sdk_level


class TestMTLFunctionLogHelper(Metal.NSObject):
    def line(self):
        pass

    def column(self):
        pass

    def type(self):  # noqa: A003
        return 1


class TestMTLFunctionLog(TestCase):
    def test_constants(self):
        self.assertEqual(Metal.MTLFunctionLogTypeValidation, 0)

    @min_sdk_level("10.16")
    def test_protocols(self):
        objc.protocolNamed("MTLLogContainer")
        objc.protocolNamed("MTLFunctionLogDebugLocation")
        objc.protocolNamed("MTLFunctionLog")

    def test_methods(self):
        self.assertResultHasType(TestMTLFunctionLogHelper.line, objc._C_NSUInteger)
        self.assertResultHasType(TestMTLFunctionLogHelper.column, objc._C_NSUInteger)
        self.assertResultHasType(TestMTLFunctionLogHelper.type, objc._C_NSInteger)
