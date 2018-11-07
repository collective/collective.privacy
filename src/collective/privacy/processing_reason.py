# -*- coding: utf-8 -*-
from zope.component.hooks import getSiteManager


class ProcessingReason(object):
    def __init__(self,
                 id,
                 identifier_factory,
                 optinoptout_storage,
                 lawful_basis,
                 title,
                 description):
        self.__name__ = id
        self.identifier_factory = identifier_factory
        self.optinoptout_storage = optinoptout_storage
        self.lawful_basis = lawful_basis
        self.Title = title
        self.Description = description

    def __repr__(self):
        return "<ProcessingReason {} using {}>".format(
            self.__name__,
            self.lawful_basis.__name__
        )

    @property
    def html_description(self):
        description = self.Description
        if self.optinoptout_storage.uses_end_user_equipment:
            description += "<p>The preference you set here will be stored on your computer.<p>"
        if not self.can_object:
            description += "<p><strong>In order to comply with Data Protection laws, we cannot offer the ability to opt out of this.</strong><p>"
        return description

    @property
    def can_object(self):
        return self.lawful_basis.can_object

    def _setValue(self, request, user, value):
        if user is not None:
            identifier = self.identifier_factory.getIdentifierForUser(user)
        else:
            identifier = self.identifier_factory.getIdentifierForCurrentRequest(request)
        if identifier is None:
            raise ValueError("Couldn't identify user")
        else:
            site = getSiteManager()
            storage = self.optinoptout_storage(self, site, request)
            if value:
                storage.consentToProcessing(identifier)
            else:
                storage.objectToProcessing(identifier)

    def consentToProcessing(self, request, user=None):
        """Mark the current user as having agreed to the processing explicitly"""
        self._setValue(request, user, True)

    def objectToProcessing(self, request, user=None):
        """Mark the current user as having refused permission to process"""
        if self.can_object:
            self._setValue(request, user, False)
        else:
            raise ValueError("Cannot object to processing {!r}".format(self))

    def isOpinionExpressed(self, request, identifier=None):
        if identifier is None:
            identifier = self.identifier_factory.getIdentifierForCurrentRequest(request)
        else:
            identifier = self.identifier_factory.getIdentifierForUser(identifier)
        if identifier is None:
            raise ValueError("Couldn't identify user")
        else:
            site = getSiteManager()
            storage = self.optinoptout_storage(self, site, request)
            value = storage.getProcessingStatus(identifier)
            return value is not None

    def isProcessingAllowed(self, request, identifier=None):
        """Return True if processing is allowed or False if not"""
        if identifier is None:
            identifier = self.identifier_factory.getIdentifierForCurrentRequest(request)
        else:
            identifier = self.identifier_factory.getIdentifierForUser(identifier)
        if identifier is None:
            raise ValueError("Couldn't identify user")
        else:
            site = getSiteManager()
            storage = self.optinoptout_storage(self, site, request)
            value = storage.getProcessingStatus(identifier)
            if value is None:
                value = self.lawful_basis.default
            return value


class MarketingProcessingReason(ProcessingReason):
    """Users can always object to processing for marketing reasons,
    regardless of the legal basis"""

    @property
    def can_object(self):
        return True


class TrackingProcessingReason(ProcessingReason):
    """Users can instruct their browsers to refuse consent on their
    behalf using the Do-Not-Track header."""

    def isOpinionExpressed(self, request, identifier=None):
        if identifier is None:
            if request.headers.get('X-Do-Not-Track'):
                return True
        return super(TrackingProcessingReason, self).isOpinionExpressed(request, identifier)

    def isProcessingAllowed(self, request, identifier=None):
        if identifier is None:
            if request.headers.get('X-Do-Not-Track'):
                return False
        return super(TrackingProcessingReason, self).isOpinionExpressed(request, identifier)


class MarketingTrackingProcessingReason(MarketingProcessingReason, TrackingProcessingReason):
    pass
