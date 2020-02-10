# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.privacy -t test_example.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.privacy.testing.COLLECTIVE_PRIVACY_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/privacy/tests/robot/test_example.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: I see the consent banner and I can consent to data use
  Given a Plone site in anonymous
   When consent has been given to My embedded media
   Then The consent banner is not visible

Scenario: I can retract my consent via consent form (banner don't show again)
  Given a Plone site in anonymous
    and consent has been given to My embedded media
   When I retract my consent
   Then The consent banner is not visible


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a Plone site in anonymous
  Go To  ${PLONE_URL}


# --- WHEN -------------------------------------------------------------------

consent has been given to My embedded media
  Go To  ${PLONE_URL}
  Element Should be visible  css=#gdpr-consent-banner
  Click Button  Allow

I retract my consent
  Go To  ${PLONE_URL}/@@consent
  Click Element  xpath=//input[@name="form.widgets.show_media_embed" and @value="Blocked"]
  Click Button  Ok


# --- THEN -------------------------------------------------------------------

The consent banner is not visible
  Element Should not be visible  css=#gdpr-consent-banner
  Go To  ${PLONE_URL}
  Element Should not be visible  css=#gdpr-consent-banner
