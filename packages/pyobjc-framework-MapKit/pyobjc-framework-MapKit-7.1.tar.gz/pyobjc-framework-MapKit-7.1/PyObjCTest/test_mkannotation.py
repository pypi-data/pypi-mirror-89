from PyObjCTools.TestSupport import TestCase, min_os_level
import objc

import MapKit


class TestMKAnnotationHelper(MapKit.NSObject):
    def coordinate(self):
        return 1

    def setCoordinate_(self, value):
        pass


class TestMKAnnotation(TestCase):
    @min_os_level("10.9")
    def testProtocols(self):
        self.assertIsInstance(objc.protocolNamed("MKAnnotation"), objc.formal_protocol)

        self.assertResultHasType(
            TestMKAnnotationHelper.coordinate, MapKit.CLLocationCoordinate2D.__typestr__
        )
        self.assertArgHasType(
            TestMKAnnotationHelper.setCoordinate_,
            0,
            MapKit.CLLocationCoordinate2D.__typestr__,
        )
