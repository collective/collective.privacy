from plone.directives import form
from zope import schema
from zope.interface import Interface
from z3c.form import button, field
from z3c.form.browser.radio import RadioFieldWidget
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage


class ConsentForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    """

    ignoreContext = True

    label = u"Privacy settings"
    description = u"Choose to opt in or out of various pieces of functionality"

    @property
    def schema(self):
        reasons = self.context.portal_privacy.getAllReasons()
        class IConsentForm(Interface):
            for reason_id, reason in reasons.items():
                if reason.identifier_factory.getIdentifierForCurrentRequest(self.request) is None:
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
                    default='Allowed' if reason.isProcessingAllowed(self.request) else 'Blocked',
                )
            del reason_id
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