Changelog
=========

1.1.0b2 (2022-01-07)
--------------------

- Fix Fixed ModuleNotFoundError: No module named 'App.class_init' on Zope 5.
  [laulaz]

- Defer the execution of consent.js (#18).
  [comwes]


1.1.0b1 (2021-08-19)
--------------------

- Fix translation domain & add translations for custom text in send_to_form email
  [laulaz]

- Fix traceback on send_to_form when sending an email : getConsentLink method
  must be accessible from template
  [laulaz]

- Fix consent banner miss (when there are multiple cookies to accept) by
  ensuring JS event is only registered once on consent banner button.
  [laulaz]

- Handle multilingual & subsites configurations by rendering consent form on
  navigation root (#15)
  [laulaz]

- Fix JSON call for banner consent to get correct language in some multilingual
  configurations, if the current language must be taken from context (#14)
  [laulaz]

- Ensure that consent banner shows on top (z-index) of everything else (eg: Google Maps)
  [laulaz]


1.1.0a1 (2020-05-12)
--------------------

- Add Python 3 and Plone 5.2 compatbility
  [mpeeters]


1.0b1 (2020-04-30)
------------------

- Avoid caching for consent banner
  [mpeeters]

- Don't show consent banner on consent form
  [laulaz]

- Allow to delete specified cookies if user objects to their use
  [laulaz]

- Add Dutch translation
  [laulaz]

- Add link to manage privacy settings
  [laulaz]

- Translate all messages / data processing reasons
  [laulaz]

- Fix consent submission
  [mpeeters]

- Fix validator for sendto_email
  [mpeeters]

- Add French translations
  [laulaz]

- Add code to give better warnings around cookie use
  [MatthewWilkes]

- Provide uninstall steps in profile (#1)
  [Mikel Larreategi]

- Possible fix for diazo compatibility
  [MatthewWilkes]

- Unintrusive analytics are legitimate
  [MatthewWilkes]

- Remove unneeded skins call
  [MatthewWilkes]

- Add missing files
  [MatthewWilkes]

- Remove unneeded deps
  [MatthewWilkes]

1.0a1 (2018-08-25)
------------------

- Initial release.
  [MatthewWilkes]
