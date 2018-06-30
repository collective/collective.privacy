# -*- coding: utf-8 -*-


class LegalBasis(object):
    def __init__(self, name, can_object, can_delete, can_port, default):
        self.__name__ = name
        self.can_object = can_object
        self.can_delete = can_delete
        self.can_port = can_port
        self.default = default


consent = LegalBasis(
    'consent',
    can_object=True,
    can_delete=True,
    can_port=True,
    default=False
)

contract = LegalBasis(
    'contract',
    can_object=False,
    can_delete=True,
    can_port=True,
    default=True
)

legal_obligation = LegalBasis(
    'legal_obligation',
    can_object=False,
    can_delete=False,
    can_port=False,
    default=True
)

legitimate_interest = LegalBasis(
    'legitimate_interest',
    can_object=True,
    can_delete=True,
    can_port=False,
    default=True
)

public_task = LegalBasis(
    'public_task',
    can_object=True,
    can_delete=False,
    can_port=False,
    default=True
)

vital_interest = LegalBasis(
    'vital_interest',
    can_object=False,
    can_delete=True,
    can_port=False,
    default=True
)
