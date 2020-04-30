.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.com/collective/collective.privacy.svg?branch=master
    :target: https://travis-ci.com/collective/collective.privacy

collective.privacy
==================

This Plone add-on adds concepts from the EU's General Data Protection Regulations
to Plone configuration, which makes it easier to create Plone sites that respect
the privacy rights of indivuals.

Features
--------

- ZCML based declaration of uses of data
- User-facing privacy management form
- Integration with core Plone features

Core Plone
----------

The following core Plone overrides are included:

* The sendto_form now validates a to email address against people who have opted-out. The legal basis
  chosen by default here is legitimate_interest.
* The analytics viewlet also relies on legitimate interest, on the basis that it assumes the tracking
  is unobtrusive and that this will be allowed by the upcoming changes to the ePrivacy regulations. If
  the tracking is obtrusive or the site owner doesn't want to make this assumption it should be overridden
  to use consent.

Examples
--------

Users can define a new data processing reason as configuration. For example, an add-on that
provides for embedding media might cause users to be tracked. The ZCML would be modified to include::


    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:gdpr="http://namespaces.plone.org/gdpr"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n_domain="collective.privacy">
        <gdpr:data_use_category
            name="show_example_media_embed"
            title="Embedded media from example.com"
            description="We use example.com to embed media into the site. example.com monitors
                         the usage patterns of users to provide enhanced analytics to site owners."
            legal_basis="consent"
            identifier="collective.privacy.identifiers.CookieIdentifier"
            storage="collective.privacy.storage.CookieStorage"
            cookies="media_cookie_*,other_cookie"
            />
    </configure>

This would add a new item to the privacy controls that relies on consent to proccess data. This means that by
default the permission is denied until an end user gives permission.

Note that the i18n domain of your configuration must be `collective.privacy` if you want to translate titles
and descriptions of your new data processing reasons. 

You can then guard your uses of the data, for example::

    <div tal:condition="python: context.portal_privacy.processingIsAllowed('show_example_media_embed')">
        ...
    </div>



Legal basis
-----------

GDPR provides for six legal bases for processing, all of which are supported by collective.privacy.

They are:

consent
*******

See: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/lawful-basis-for-processing/consent/

Processing is disallowed by default, users can opt-in. There are rules as to what makes consent valid, which must be followed.

contract
********

See: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/lawful-basis-for-processing/contract/

Processing is allowed and users cannot object.


legal_obligation
****************

See: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/lawful-basis-for-processing/legal-obligation/

Processing is allowed and users cannot object.

vital_interest
****************

See: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/lawful-basis-for-processing/vital-interests/

Processing is allowed and users cannot object.

public_task
***********

See: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/lawful-basis-for-processing/public-task/

Processing is allowed by default, but users may object. This is only suitable for certain specific types of processing.

legitimate_interest
*******************

See: https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/lawful-basis-for-processing/legitimate-interests/

Processing is allowed by default, but users may object.


Identifiers
-----------

It is necessary to tell one user from another when managing their preferences. In some cases different
identifiers are more useful than others. For example, when sending email we want to key users on the
email address, but using cookies should be managed by the browser, regardless of the user's logged in state.

The way of choosing which is used is called a identifier. The following are available:

collective.privacy.identifiers.CookieIdentifier
***********************************************

This identifier should be used in cases where the storage is cookie based. It allows the current user
to be identifier, but not other arbitrary users.

collective.privacy.identifiers.EmailIdentifier
**********************************************

This identifier should be used when the user needs to be identified by email address. It can optionally
use the email address of a logged in user to identify the current request, but in general it cannot
identify the current user.

The identifier is a UUID derived from the email address using a one-way function, not the email itself.

collective.privacy.identifiers.IPIdentifier
*******************************************

This identifier should be used to identify a connection. It can be used to identify the current user or
other arbitrary users. It is less reliable than the CookieIdentifier as users IP addresses can change.

The identifier is a UUID derived from the IP address using a one-way function, not the IP itself.

collective.privacy.identifiers.UserIdentifier
*********************************************

This identifier can only be used to identify logged-in users. It can identify any users who are registered
on the site, but not anonymous visitors. As such, it's appropriate for data processing that only occurs
for registered users.

The identifier is a UUID derived from the user name using a one-way function, not the username itself.

Storages
--------

The storage determines how the user's preferences are persisted. There are three storages available:

collective.privacy.storage.CookieStorage
****************************************

This storage uses a cookie called 'dataprotection' on the user's browser. Consent is not required
to set this cookie as it is set to comply with legal obligations and cannot be used to track the user.

collective.privacy.storage.DatabaseStorage
******************************************

This storage uses BTrees inside the portal_privacy tool to store the time the user consented or objected.
It is currently the only storage that allows for the preferences of users to be queried outside of a request
they have initiated.

collective.privacy.storage.NoChoiceStorage
******************************************

This is a stub storage to be used with legal bases such as vital_interest where the user has no option
to object to processing.


Cookies
-------

This attribute lists the cookies that should be deleted if the user objects to the use of the corresponding data processing.
It is optional and may contain wildcard (*).


Translations
------------

This product has been translated into

- French
- Dutch


Installation
------------

Install collective.privacy by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.privacy


and then running ``bin/buildout``

Varnish
-------

If you use this product combined with Varnish ensure that your Varnish config does not remove cookies for requests where
caching should be ignored

Example of config::

    if (req.http.Cache-Control ~ "(private|no-cache|no-store)" || req.http.Pragma == "no-cache") {
        return (pass);
    }


Thanks
------

Thanks to Jazkarta ( http://jazkarta.com/ ) and YES! Magazine ( http://www.yesmagazine.org/ ) for
each sponsoring some of the development costs of this add-on.

The irony that these are both US companies is not lost on us.

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.privacy/issues
- Source Code: https://github.com/collective/collective.privacy


Support
-------

If you are having issues, please let us know.

License
-------

The project is licensed under the GPLv2.

N.B., the GPL states:

    THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
    PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
    OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
    TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
    PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
    REPAIR OR CORRECTION.

This add-on has not received any contributors from lawyers and should not be
interpreted as legal advice.
