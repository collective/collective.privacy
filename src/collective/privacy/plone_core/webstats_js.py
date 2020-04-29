# -*- coding: utf-8 -*-
from plone.app.layout.analytics.view import AnalyticsViewlet
from zope.interface import implementer
from zope.viewlet.interfaces import IViewlet


@implementer(IViewlet)
class PrivacyRespectingAnalyticsViewlet(AnalyticsViewlet):
    def render(self):
        """render the webstats snippet"""
        if self.context.portal_privacy.processingIsAllowed("basic_analytics"):
            return super(PrivacyRespectingAnalyticsViewlet, self).render()
        else:
            return ""
