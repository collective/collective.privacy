# -*- coding: utf-8 -*-
from zope.component._api import getSiteManager
from zope.configuration.fields import GlobalObject
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.schema import Bool, TextLine

from collective.privacy.interfaces import ILawfulBasis, IProcessingReason
from collective.privacy.processing_reason import MarketingProcessingReason, ProcessingReason

_ = MessageFactory('collective.privacy')


class IDataUseCategory(Interface):
    """
    Register an adapter
    """

    name = TextLine(
        title=_("Name"),
        description=_("Adapters can have names.\n\n"
                      "This attribute allows you to specify the name for"
                      " this adapter."),
        required=False,
    )

    legal_basis = TextLine(
        title=_("Legal basis"),
        description=_("The identifier of a legal basis that is used here"),
        required=True,
    )

    identifier = GlobalObject(
        title=_("How users will be identified"),
        description=_("An object that provides IIdentifierFactory"),
        required=True,
    )

    storage = GlobalObject(
        title=_("Storage for this data"),
        description=_("An object that provides IOptInOptOutStorage"),
        required=True,
    )

    title = TextLine(
        title=_("Title"),
        description=_("The end-user visible name for this processing"),
        required=False,
    )

    description = TextLine(
        title=_("Description"),
        description=_("The end-user visible description of this processing"),
        required=False,
    )

    marketing = Bool(
        title=_("Marketing"),
        description=_("Is this used for marketing purposes?"),
        required=False,
        default=False,
    )


def data_use_category(_context, name, title, description, legal_basis, storage, identifier, marketing=False):
    _context.action(
        discriminator=('processing_reason', name),
        callable=register_data_use_category,
        args=(name, title, description, legal_basis, storage, identifier),
    )
    return


def register_data_use_category(name, title, description, legal_basis, storage, identifier, marketing=False):
    manager = getSiteManager()
    legal_basis_obj = manager.queryUtility(ILawfulBasis, name=legal_basis)
    if legal_basis_obj is None:
        raise ValueError('{} is not a valid lawful basis.'.format(legal_basis))

    if marketing:
        kls = MarketingProcessingReason
    else:
        kls = ProcessingReason
    reason = kls(
        id=name,
        title=title,
        description=description,
        lawful_basis=legal_basis_obj,
        optinoptout_storage=storage,
        identifier_factory=identifier,
    )
    manager.registerUtility(reason, IProcessingReason, name)
