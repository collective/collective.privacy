# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface, Attribute
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectivePrivacyLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPrivacyTool(Interface):
    pass


class IIdentifierFactory(Interface):
    __name__ = Attribute("An identifier for this identifier factory")

    def getIdentifierForCurrentRequest(request):
        """Return the identifier integer for the current user"""
        NotImplemented

    def getIdentifierForUser(user):
        """Return an identifier for a factory-specific input, such as
        email address, IP, Plone user. This must be an integer."""


class ILawfulBasis(Interface):
    __name__ = Attribute("An identifier for this basis")
    can_object = Attribute("The data subject can request no processing")
    can_delete = Attribute("The data subject can request deletion")
    can_port = Attribute("The data subject can move this data to a new provider")
    default = Attribute("True if processing is allowed by default (consent), otherwise False")


class IProcessingReason(Interface):
    """This represents a reason for processing data in a site"""
    __name__ = Attribute("An identifier for this category")

    identifier_factory = Attribute("Which method to use to identify a user")
    optinoptout_storage = Attribute("Which method to use to store data")
    lawful_basis = Attribute("Which lawful basis is being relied on")

    Title = Attribute("The name of this category, visible to users")
    Description = Attribute("A description of the usage of this data, for end users")

    def consentToProcessing(request):
        """Mark the current user as having agreed to the processing explicitly"""
        NotImplemented

    def objectToProcessing(request):
        """Mark the current user as having refused permission to process"""
        NotImplemented

    def isProcessingAllowed(request, identifier):
        """Return True if processing is allowed or False if not. If identifier is provided
        the user represented by that identifier is used, otherwise it's the current request
        user"""
        NotImplemented


class IOptInOptOutStorage(Interface):
    processing_reason = Attribute("The processing reason for this data")
    context = Attribute("The database location for storage")
    request = Attribute("The current request")

    def __init__(processing_reason, site_root, request):
        pass

    def consentToProcessing(identifier):
        NotImplemented

    def objectToProcessing(identifier):
        NotImplemented

    def getProcessingStatus(identifier):
        """Returns True if user has consented, False if they've objected and None if
        there is no data"""
        NotImplemented
