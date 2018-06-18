# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.privacy.testing import COLLECTIVE_PRIVACY_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.privacy is properly installed."""

    layer = COLLECTIVE_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.privacy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.privacy'))

    def test_browserlayer(self):
        """Test that ICollectivePrivacyLayer is registered."""
        from collective.privacy.interfaces import (
            ICollectivePrivacyLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectivePrivacyLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PRIVACY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.privacy'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.privacy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.privacy'))

    def test_browserlayer_removed(self):
        """Test that ICollectivePrivacyLayer is removed."""
        from collective.privacy.interfaces import \
            ICollectivePrivacyLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectivePrivacyLayer,
            utils.registered_layers())
