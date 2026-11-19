"""Setup tests for this package."""

from collective.privacy.testing import (  # noqa: E501
    COLLECTIVE_PRIVACY_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.utils import get_installer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.privacy is properly installed."""

    layer = COLLECTIVE_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.privacy is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.privacy"))

    def test_browserlayer(self):
        """Test that ICollectivePrivacyLayer is registered."""
        from collective.privacy.interfaces import ICollectivePrivacyLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectivePrivacyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.privacy")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.privacy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("collective.privacy"))

    def test_browserlayer_removed(self):
        """Test that ICollectivePrivacyLayer is removed."""
        from collective.privacy.interfaces import ICollectivePrivacyLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectivePrivacyLayer, utils.registered_layers())

    def test_configuration_registry_removed(self):
        """Test that registry keys added to the configuration registry
        are removed."""
        registry = getUtility(IRegistry)
        self.assertNotIn("collective.privacy.trust_member_emails", registry)
        self.assertNotIn("collective.privacy.solicit_consent", registry)

    def test_privacy_tool_not_in_site_root(self):
        """Test that the privacy tool is uninstalled"""
        self.assertNotIn("privacy_tool", self.portal)
