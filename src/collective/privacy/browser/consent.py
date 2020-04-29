# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from collective.privacy import _
from collective.privacy.interfaces import IConsentFormView
from plone import api
from plone.app.layout.viewlets import common as base
from plone.directives import form
from z3c.form import button
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import json

consent_values = SimpleVocabulary(
    [
        SimpleTerm(value=u"Allowed", title=_(u"Allowed")),
        SimpleTerm(value=u"Blocked", title=_(u"Blocked")),
    ]
)


@implementer(IConsentFormView)
class ConsentForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@consent

    """

    ignoreContext = True

    label = _(u"Privacy settings")
    description = _(u"Choose to opt in or out of various pieces of functionality")

    @property
    def action(self):
        return self._action

    @property
    def schema(self):
        reasons = self.context.portal_privacy.getAllReasons()
        validated_user = None
        self._action = self.url(name="consent")
        if "user_id" in self.request.form:
            processing_reason = self.request.form.get("processing_reason")
            user_id = self.request.form.get("user_id")
            authentication = self.request.form.get("authentication")
            if self.context.portal_privacy.verifyIdentifier(
                authentication, processing_reason, user_id
            ):
                reason_object = self.context.portal_privacy.getProcessingReason(
                    processing_reason
                )
                validated_user = (reason_object.identifier_factory.__name__, user_id)
                self._action = self.url(
                    name="consent",
                    data={
                        "processing_reason": processing_reason,
                        "user_id": user_id,
                        "authentication": authentication,
                    },
                )

        class IConsentForm(Interface):
            lang = api.portal.get_current_language()
            for reason_id, reason in sorted(reasons.items()):
                reason_match = (
                    validated_user
                    and validated_user[0] == reason.identifier_factory.__name__
                )
                if reason_match:
                    if (
                        reason.identifier_factory.getIdentifierForUser(
                            validated_user[1]
                        )
                        is None
                    ):
                        continue
                elif (
                    reason.identifier_factory.getIdentifierForCurrentRequest(
                        self.request
                    )
                    is None
                ):
                    continue
                reason_id = reason_id.encode("ascii", "replace")
                form.widget(reason_id, RadioFieldWidget)
                if not reason.can_object:
                    form.mode(**{reason_id: "display"})
                translated_title = translate(_(reason.Title), target_language=lang)
                locals()[reason_id] = schema.Choice(
                    title=translated_title,
                    description=reason.html_description,
                    vocabulary=consent_values,
                    required=True,
                    default="Allowed"
                    if reason.isProcessingAllowed(
                        self.request,
                        identifier=validated_user[1] if reason_match else None,
                    )
                    else "Blocked",
                )
            del lang
            del translated_title
            del reason_id
            del reason_match
            del reason

        return IConsentForm

    @button.buttonAndHandler(_(u"Ok"))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        privacy_tool = self.context.portal_privacy
        for topic, answer in data.items():
            answer = answer == "Allowed"
            if answer:
                privacy_tool.consentToProcessing(topic)
            else:
                privacy_tool.objectToProcessing(topic)

        self.status = _(u"Your preferences have been saved.")

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """


class ConsentBannerViewlet(base.ViewletBase):
    def is_consent_required(self):
        if not api.portal.get_registry_record("collective.privacy.solicit_consent"):
            return False
        if IConsentFormView.providedBy(self.view):
            # Don't show consent banner on consent form
            return False
        consent_reasons = [
            reason
            for reason in self.context.portal_privacy.getAllReasons().values()
            if reason.lawful_basis.__name__ == "consent"
        ]
        return len(consent_reasons) > 0


class ConsentJSON(BrowserView):
    """
    This view return a json for opinions required for the current user based on
    collective.privacy cookie
    """

    def __call__(self):
        found = []
        self.request.response.setHeader("Content-type", "application/json")
        consent_reasons = [
            reason
            for reason in self.context.portal_privacy.getAllReasons().values()
            if reason.lawful_basis.__name__ == "consent"
        ]
        for reason in consent_reasons:
            try:
                if not reason.isOpinionExpressed(self.request):
                    found.append(
                        {
                            "Title": translate(_(reason.Title), context=self.request),
                            "Description": translate(
                                _(reason.Description), context=self.request
                            ),
                            "name": reason.__name__,
                        }
                    )
            except Exception:
                # FIXME
                pass
        return json.dumps(found)
