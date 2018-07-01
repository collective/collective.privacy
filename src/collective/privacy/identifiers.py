# -*- coding: utf-8 -*-
import uuid

from plone import api


class CookieIdentifier(object):
    __name__ = "cookie"

    @classmethod
    def getIdentifierForCurrentRequest(kls, request):
        """ It is not possible to get the user's email address from a request"""
        return "current"

    @classmethod
    def getIdentifierForUser(kls, user):
        return None


class EmailIdentifier(object):
    __name__ = "Email"
    NAMESPACE = uuid.UUID('a838b36d-d1d5-477e-8471-c1e2079417cf')

    @classmethod
    def getIdentifierForCurrentRequest(kls, request):
        """ It is not possible to get the user's email address from a request"""
        try:
            if api.portal.get_registry_record('collective.privacy.trust_member_emails'):
                email = api.user.get_current().getProperty('email')
            else:
                email = None
            if not email:
                return None
            return kls.getIdentifierForUser(email)
        except:
            return None

    @classmethod
    def getIdentifierForUser(kls, user):
        """Use UUID5 to get an integer ID in a namespace"""
        return uuid.uuid5(kls.NAMESPACE, user).int


class IPIdentifier(object):
    __name__ = "IP"
    NAMESPACE = uuid.UUID('45865cac-1e4f-46d3-8e3e-1c277db76f3e')

    @classmethod
    def get_ip(seklslf, request):
        """ Extract the client IP address from the HTTP request in a proxy-compatible way.

        @return: IP address as a string or None if not available
        """
        if "HTTP_X_FORWARDED_FOR" in request.environ:
            # Virtual host
            ip = request.environ["HTTP_X_FORWARDED_FOR"]
        elif "HTTP_HOST" in request.environ:
            # Non-virtualhost
            ip = request.environ["REMOTE_ADDR"]
        else:
            # Unit test code?
            ip = None
        return ip

    @classmethod
    def getIdentifierForCurrentRequest(kls, request):
        """ It is not possible to get the user's email address from a request"""
        return kls.getIdentifierForUser(kls.get_ip(request))

    @classmethod
    def getIdentifierForUser(kls, user):
        """Use UUID5 to get an integer ID in a namespace"""
        return uuid.uuid5(kls.NAMESPACE, user).int


class UserIdentifier(object):
    __name__ = "User"
    NAMESPACE = uuid.UUID('9d01c079-a268-4e43-81f7-0eecd4c45316')

    @classmethod
    def getIdentifierForCurrentRequest(kls, request):
        """ It is not possible to get the user's email address from a request"""
        username = api.user.get_current().getUserName()
        if not username:
            return None
        return kls.getIdentifierForUser(username)

    @classmethod
    def getIdentifierForUser(kls, user):
        """Use UUID5 to get an integer ID in a namespace"""
        return uuid.uuid5(kls.NAMESPACE, user).int


class NoChoiceIdentifier(object):
    __name__ = "NoChoice"

    @classmethod
    def getIdentifierForCurrentRequest(kls, request):
        """ It is not possible to get the user's email address from a request"""
        return 0

    @classmethod
    def getIdentifierForUser(kls, user):
        """Use UUID5 to get an integer ID in a namespace"""
        return 0
