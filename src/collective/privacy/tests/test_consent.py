"""Consent form and consent JSON tests."""

from collective.privacy.interfaces import ICollectivePrivacyLayer
from collective.privacy.testing import COLLECTIVE_PRIVACY_INTEGRATION_TESTING
from zope.interface import alsoProvides

import json
import unittest


class TestConsent(unittest.TestCase):

    layer = COLLECTIVE_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, ICollectivePrivacyLayer)

    def test_consent_form_lists_reasons(self):
        form = self.portal.restrictedTraverse("@@consent")
        html = form()
        self.assertIn("form.widgets.show_media_embed", html)
        self.assertIn("form.widgets.basic_analytics", html)
        self.assertEqual(form.action, "http://nohost/plone/consent")

    def test_consent_json_lists_unanswered_consent_reasons(self):
        view = self.portal.restrictedTraverse("@@consent-json")
        names = [reason["name"] for reason in json.loads(view())]
        self.assertEqual(names, ["show_media_embed"])
