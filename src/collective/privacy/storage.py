# -*- coding: utf-8 -*-

import time
from email.Utils import formatdate

from .tool import ProcessingReason


class BaseStorage(object):

    def __init__(self, processing_reason, site_root, request):
        self.context = site_root
        self.request = request
        self.processing_reason = processing_reason

    def getCurrentIdentifier(self):
        return self.processing_reason.identifier_factory.getIdentifierForCurrentRequest(self.request)


class CookieStorage(BaseStorage):

    def consentToProcessing(self, identifier):
        if identifier != self.getCurrentIdentifier():
            raise ValueError("Cannot consent to processing for a user other than the current")
        return self._setProcessingCookie(True)

    def objectToProcessing(self, identifier):
        if identifier != self.getCurrentIdentifier():
            raise ValueError("Cannot object to processing for a user other than the current")
        return self._setProcessingCookie(False)

    def getProcessingStatus(self, identifier):
        """Returns True if user has consented, False if they've objected and None if
        there is no data"""
        if identifier != self.getCurrentIdentifier():
            raise ValueError("Cannot check processing data outside an active request for the user concerned")
        if 'dataprotection' in self.request.RESPONSE.cookies:
            # If this request changed the settings we use that in preference of the old ones
            cookies = self.request.RESPONSE.cookies.get('dataprotection').get('value')
        else:
            cookies = self.request.cookies.get('dataprotection', '')
        cookies = cookies.split(':')
        if '{}|1'.format(self.processing_reason.__name__) in cookies:
            return True
        elif '{}|0'.format(self.processing_reason.__name__) in cookies:
            return False
        else:
            return None

    def _setProcessingCookie(self, shouldProcess):
        topic = self.processing_reason.__name__
        try:
            existing_cookies = self.request.RESPONSE.cookies['dataprotection']['value']
        except KeyError:
            existing_cookies = self.request.cookies.get('dataprotection', '')
        existing_cookies = existing_cookies.split(':')
        existing_cookies = filter(None, existing_cookies)
        existing_cookies = filter(
            lambda cookie: '{}|'.format(topic) not in cookie,
            existing_cookies
        )
        new_cookie = '{}|{:d}'.format(topic, int(shouldProcess))
        cookie = ':'.join(existing_cookies + [new_cookie])
        expiration_seconds = time.time() + (60*60*24*365)
        expires = formatdate(expiration_seconds, usegmt=True) 
        self.request.RESPONSE.setCookie('dataprotection', cookie, path='/', expires=expires)


class DatabaseStorage(BaseStorage):

    def __init__(self, processing_reason, site_root, request):
        privacy_tool = site_root.portal_privacy
        reason_id = processing_reason.__name__.encode('ascii', 'ignore')
        if reason_id not in privacy_tool.objectIds():
            privacy_tool._setObject(
                reason_id,
                ProcessingReason(id=reason_id),
            )
        self.context = privacy_tool[reason_id]
        self.request = request
        self.processing_reason = processing_reason

    def consentToProcessing(self, identifier):
        self.context.consented[identifier] = time.time()
        try:
            del self.context.objected[identifier]
        except KeyError:
            pass

    def objectToProcessing(self, identifier):
        try:
            del self.context.consented[identifier]
        except KeyError:
            pass
        self.context.objected[identifier] = time.time()

    def getProcessingStatus(self, identifier):
        if identifier in self.context.consented:
            return True
        elif identifier in self.context.objected:
            return False
        else:
            return None


class NoChoiceStorage(BaseStorage):
    """This represents a storage where the legal basis does not
    allow for the user to opt out, viz Contract, Legal Obligation and
    Vital interest.

    It should not be used for other bases."""

    def __init__(self, processing_reason, site_root, request):
        self.context = site_root
        self.request = request
        self.processing_reason = processing_reason
        if processing_reason.lawful_basis.can_object:
            raise ValueError("NoChoiceStorage is not suitable for lawful bases where objection is allowed")

    def consentToProcessing(self, identifier):
        return

    def objectToProcessing(self, identifier):
        return

    def getProcessingStatus(self, identifier):
        return True
