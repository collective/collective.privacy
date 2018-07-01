# -*- coding: utf-8 -*-
import hmac
import uuid

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees.OOBTree import OOBTree
from Products.CMFCore.utils import UniqueObject
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from OFS.SimpleItem import SimpleItem
from OFS.ObjectManager import IFAwareObjectManager
from OFS.OrderedFolder import OrderedFolder
from zope.component import getUtility
from zope.component import getUtilitiesFor

from collective.privacy.interfaces import IProcessingReason


class ProcessingReason(SimpleItem):

    def __init__(self, id, *args, **kwargs):
        super(ProcessingReason, self).__init__(*args, **kwargs)
        self.id = id
        self.consented = OOBTree()  # LFBtree only supports some longs, not all and there is no OFBTree
        self.objected = OOBTree()

    def __repr__(self):
        return "<ProcessingReason at {}>".format('/'.join(self.absolute_path()))

    def getId(self):
        return self.id


InitializeClass(ProcessingReason)


class PrivacyTool(UniqueObject, IFAwareObjectManager, OrderedFolder, PloneBaseTool):
    """ Manage through-the-web signup policies.
    """

    meta_type = 'Plone Privacy Tool'
    _product_interfaces = (IProcessingReason,)
    security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/pencil_icon.png'
    id = 'portal_privacy'
    plone_tool = 1

    def _setId(self, *args, **kwargs):
        return

    def getId(self):
        return 'portal_privacy'

    def __init__(self, *args, **kwargs):
        super(PrivacyTool, self).__init__(self, *args, **kwargs)
        self._signing_secret = uuid.uuid4().hex

    def signIdentifier(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        if user is None:
            identifier = processing_reason.identifier_factory.getIdentifierForCurrentRequest(self.REQUEST)
        else:
            identifier = processing_reason.identifier_factory.getIdentifierForUser(user)
        if identifier is None:
            raise ValueError("Couldn't identify user")
        return hmac.new(
            self._signing_secret,
            msg=str(identifier)
        ).hexdigest()

    def verifyIdentifier(self, signed, processing_reason_id, user=None):
        return hmac.compare_digest(
            signed,
            self.signIdentifier(processing_reason_id, user)
        )

    def getConsentLink(self, processing_reason_id, user=None):
        site = self.portal_url.getPortalObject()
        return "{}/@@consent?processing_reason={}&user_id={}&authentication={}".format(
            site.absolute_url(),
            processing_reason_id,
            user,
            self.signIdentifier(processing_reason_id, user)
        )

    def bannerConsent(self, processing_reason, consent=None, refuse=None):
        """User-accessible consent action"""
        if consent:
            self.consentToProcessing(processing_reason)
        elif refuse:
            self.objectToProcessing(processing_reason)
        return

    def getAllReasons(self):
        return dict(getUtilitiesFor(IProcessingReason))

    def getProcessingReason(self, processing_reason_id):
        return getUtility(IProcessingReason, name=processing_reason_id)

    def processingIsAllowed(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        return processing_reason.isProcessingAllowed(self.REQUEST, user)

    def objectToProcessing(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        processing_reason.objectToProcessing(request=self.REQUEST, user=user)

    def consentToProcessing(self, processing_reason_id, user=None):
        processing_reason = self.getProcessingReason(processing_reason_id)
        processing_reason.consentToProcessing(request=self.REQUEST, user=user)

    def requestPorting(self, identifier, topic=None):
        raise NotImplementedError

    def requestDeletion(self, identifier, topic=None):
        raise NotImplementedError


InitializeClass(PrivacyTool)
