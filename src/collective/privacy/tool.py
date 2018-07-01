# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from BTrees.OIBTree import OIBTree
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
        self.consented = OIBTree()
        self.objected = OIBTree()

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
