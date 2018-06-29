from Products.CMFPlone.browser.interfaces import ISendToForm
from z3c.form import field
from z3c.form import validator


class SendToEmailValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super(SendToEmailValidator, self).validate(value)
        import pdb; pdb.set_trace()

sendto_email = SendToEmailValidator(
    None,
    None,
    None,
    ISendToForm['send_to_address'],
    None
)
