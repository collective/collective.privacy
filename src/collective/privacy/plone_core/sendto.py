from Products.CMFPlone.browser.interfaces import ISendToForm
from z3c.form import validator
from zope.interface import Invalid


class SendToEmailValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super().validate(value)
        if value and not self.context.portal_privacy.processingIsAllowed(
            "send_to_form", user=value
        ):
            raise Invalid("This person does not want to receive our emails")


validator.WidgetValidatorDiscriminators(
    SendToEmailValidator, field=ISendToForm["send_to_address"]
)
