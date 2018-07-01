# -*- coding: utf-8 -*-
from Products.CMFPlone.browser.interfaces import ISendToForm
from z3c.form import validator
from zope.interface import Invalid


class SendToEmailValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super(SendToEmailValidator, self).validate(value)
        if value and not self.context.portal_privacy.processingIsAllowed('send_to_form', user=value):
            raise Invalid(u'This person does not want to receive our emails')


sendto_email = SendToEmailValidator(
    None,
    None,
    None,
    ISendToForm['send_to_address'],
    None
)
