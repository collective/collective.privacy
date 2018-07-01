from plone import api
from plone.directives import form
from zope import schema
from zope.interface import Interface
from z3c.form import button, field
from z3c.form.browser.radio import RadioFieldWidget
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.viewlets import common as base


class ConsentForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    """

    ignoreContext = True

    label = u"Privacy settings"
    description = u"Choose to opt in or out of various pieces of functionality"

    @property
    def action(self):
        return self._action

    @property
    def schema(self):
        reasons = self.context.portal_privacy.getAllReasons()
        validated_user = None
        self._action = self.url(name="consent")
        if 'user_id' in self.request.form:
            processing_reason = self.request.form.get('processing_reason')
            user_id = self.request.form.get('user_id')
            authentication = self.request.form.get('authentication')
            if self.context.portal_privacy.verifyIdentifier(
                authentication,
                processing_reason,
                user_id
            ):
                reason_object = self.context.portal_privacy.getProcessingReason(processing_reason)
                validated_user = (
                    reason_object.identifier_factory.__name__,
                    user_id
                )
                self._action = self.url(
                    name="consent",
                    data={
                        'processing_reason': processing_reason,
                        'user_id': user_id,
                        'authentication': authentication,
                    }
                )

        class IConsentForm(Interface):
            for reason_id, reason in sorted(reasons.items()):
                reason_match = validated_user and validated_user[0] == reason.identifier_factory.__name__
                if reason_match:
                    if reason.identifier_factory.getIdentifierForUser(validated_user[1]) is None:
                        continue
                elif reason.identifier_factory.getIdentifierForCurrentRequest(self.request) is None:
                    continue
                reason_id = reason_id.encode('ascii', 'replace')
                form.widget(reason_id, RadioFieldWidget)
                if not reason.lawful_basis.can_object:
                    form.mode(**{reason_id:'display'})
                locals()[reason_id] = schema.Choice(
                    title=reason.Title,
                    description=reason.Description,
                    values=('Allowed', 'Blocked'),
                    required=True,
                    default='Allowed' if reason.isProcessingAllowed(self.request, identifier=validated_user[1] if reason_match else None) else 'Blocked',
                )
            del reason_id
            del reason_match
            del reason
        return IConsentForm

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        privacy_tool = self.context.portal_privacy
        for topic, answer in data.items():
            answer = answer == 'Allowed'
            if answer:
                privacy_tool.consentToProcessing(topic)
            else:
                privacy_tool.objectToProcessing(topic)

        self.status = "Your preferences have been saved."

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """


class ConsentBannerViewlet(base.ViewletBase):

    def getConsentRequired(self):
        found = []
        if not api.portal.get_registry_record('collective.privacy.solicit_consent'):
            return found
        consent_reasons = [
            reason
            for reason in self.context.portal_privacy.getAllReasons().values()
            if reason.lawful_basis.__name__ == 'consent'
        ]
        for reason in consent_reasons:
            try:
                if not reason.isOpinionExpressed(self.request):
                    found.append(reason)
            except:
                pass
        return found