# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.viewlet.interfaces import IViewlet

from plone.app.layout.analytics.view import AnalyticsViewlet


@implementer(IViewlet)
class PrivacyRespectingAnalyticsViewlet(AnalyticsViewlet):

    def render(self):
        """render the webstats snippet"""
        if self.context.portal_privacy.processingIsAllowed('basic_analytics'):
            return super(PrivacyRespectingAnalyticsViewlet, self).render()
        else:
            return ""
