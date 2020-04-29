# -*- coding: utf-8 -*-
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.privacy


class CollectivePrivacyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.privacy, name="testing.zcml")
        self.loadZCML(package=collective.privacy.tests, name="data_use.zcml")

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.privacy:default")
        api.portal.set_registry_record("collective.privacy.solicit_consent", True)


COLLECTIVE_PRIVACY_FIXTURE = CollectivePrivacyLayer()


COLLECTIVE_PRIVACY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PRIVACY_FIXTURE,),
    name="CollectivePrivacyLayer:IntegrationTesting",
)


COLLECTIVE_PRIVACY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PRIVACY_FIXTURE,), name="CollectivePrivacyLayer:FunctionalTesting"
)


COLLECTIVE_PRIVACY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PRIVACY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectivePrivacyLayer:AcceptanceTesting",
)
