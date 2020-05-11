# -*- coding: utf-8 -*-
"""Cookies tests for this package."""
from collective.privacy.testing import COLLECTIVE_PRIVACY_INTEGRATION_TESTING
from zope.globalrequest import getRequest

import unittest
import re

COOKIES = {"foo1": "foo value", "foo2": "foo value 2", "bar": "bar value"}


class TestCookies(unittest.TestCase):
    """Test collective.privacy cookie manipulation."""

    layer = COLLECTIVE_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]

    def test_expire_data_use_cookies(self):
        """ Test that cookies for data use expires after user objects """
        consent_reason = [
            reason
            for reason in self.portal.portal_privacy.getAllReasons().values()
            if reason.lawful_basis.__name__ == "consent"
            and reason.__name__ == "show_media_embed"
        ][0]
        request = getRequest()
        request.cookies = COOKIES
        consent_reason.objectToProcessing(request)
        cookies = request.response.cookies
        for cookie_name in COOKIES:
            self.assertIn(cookie_name, cookies)
            data = cookies.get(cookie_name)
            self.assertEqual(data["value"], "deleted")
            self.assertEqual(data["max_age"], 0)
            # Depending of the version of Plone and Zope, the result differ
            # Wed, 31 Dec 1997 23:59:59 GMT on Plone 5.2
            # Wed, 31-Dec-97 23:59:59 GMT before
            expire_regexp = "Wed, 31( |-)Dec( |-)(1997|97) 23:59:59 GMT"
            self.assertIsNotNone(re.match(expire_regexp, data["expires"]))
