from PyObjCTools.TestSupport import TestCase, min_os_level
import objc
import Contacts


class TestContacts(TestCase):
    @min_os_level("10.11")
    def testClasses(self):
        self.assertIsInstance(Contacts.CNContact, objc.objc_class)
