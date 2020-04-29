# -*- coding: utf-8 -*-
from collective.privacy import _
from collective.privacy.interfaces import ILawfulBasis
from collective.privacy.interfaces import IProcessingReason
from collective.privacy.processing_reason import MarketingProcessingReason
from collective.privacy.processing_reason import MarketingTrackingProcessingReason
from collective.privacy.processing_reason import ProcessingReason
from collective.privacy.processing_reason import TrackingProcessingReason
from zope.component._api import getSiteManager
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import TextLine


class IDataUseCategory(Interface):
    """
    Register a data use category
    """

    name = TextLine(
        title=_("Name"), description=_("The id used for this category."), required=False
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
        description=_("The end-user visible title for this processing"),
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

    tracking = Bool(
        title=_("Tracking"),
        description=_("Is this used for tracking purposes?"),
        required=False,
        default=False,
    )

    cookies = TextLine(
        title=_("Cookies names"),
        description=_(
            "List of cookies for this use : separeted by ',', wildcard (*) accepted"
        ),
        required=False,
    )


def data_use_category(
    _context,
    name,
    title,
    description,
    legal_basis,
    storage,
    identifier,
    marketing=False,
    tracking=False,
    cookies=u"",
):
    _context.action(
        discriminator=("processing_reason", name),
        callable=register_data_use_category,
        args=(
            name,
            title,
            description,
            legal_basis,
            storage,
            identifier,
            marketing,
            tracking,
            cookies,
        ),
    )
    return


def register_data_use_category(
    name,
    title,
    description,
    legal_basis,
    storage,
    identifier,
    marketing=False,
    tracking=False,
    cookies=u"",
):
    manager = getSiteManager()
    legal_basis_obj = manager.queryUtility(ILawfulBasis, name=legal_basis)
    if legal_basis_obj is None:
        raise ValueError("{} is not a valid lawful basis.".format(legal_basis))

    if marketing and tracking:
        kls = MarketingTrackingProcessingReason
    elif marketing:
        kls = MarketingProcessingReason
    elif tracking:
        kls = TrackingProcessingReason
    else:
        kls = ProcessingReason
    reason = kls(
        id=name,
        title=title,
        description=description,
        lawful_basis=legal_basis_obj,
        optinoptout_storage=storage,
        identifier_factory=identifier,
        cookies=cookies,
    )
    manager.registerUtility(reason, IProcessingReason, name)
