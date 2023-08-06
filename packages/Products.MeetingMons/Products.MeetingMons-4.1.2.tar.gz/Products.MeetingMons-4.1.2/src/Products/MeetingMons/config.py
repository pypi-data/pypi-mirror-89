# -*- coding: utf-8 -*-
#
# File: config.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
from collections import OrderedDict

__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'

# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
from Products.PloneMeeting import config as PMconfig

PROJECTNAME = "MeetingMons"

MONSROLES = {}
MONSROLES['budgetimpactreviewers'] = 'MeetingBudgetImpactReviewer'
MONSROLES['serviceheads'] = 'MeetingServiceHead'
MONSROLES['officemanagers'] = 'MeetingOfficeManager'
MONSROLES['extraordinarybudget'] = 'MeetingExtraordinaryBudget'
MONSROLES['divisionheads'] = 'MeetingDivisionHead'
PMconfig.MEETINGROLES.update(MONSROLES)

MONSMEETINGREVIEWERS = {
    "meetingitemcollegemons_workflow": OrderedDict(
        [
            ('reviewers', ['proposed_to_director']),
            ('divisionheads', ['proposed_to_divisionhead']),
            ('officemanagers', ['proposed_to_officemanager']),
            ('serviceheads', ['proposed_to_servicehead']), ]
    ),
}
PMconfig.MEETINGREVIEWERS = MONSMEETINGREVIEWERS

PMconfig.EXTRA_GROUP_SUFFIXES = [
    {"fct_title": u"divisionheads", "fct_id": u"divisionheads", "fct_orgs": [], 'enabled': True},
    {"fct_title": u"officemanagers", "fct_id": u"officemanagers", "fct_orgs": [], 'enabled': True},
    {"fct_title": u"serviceheads", "fct_id": u"serviceheads", "fct_orgs": [], 'enabled': True},
    {"fct_title": u"extraordinarybudget", "fct_id": u"extraordinarybudget", "fct_orgs": [],
     'enabled': True},
    {"fct_title": u"budgetimpactreviewers", "fct_id": u"budgetimpactreviewers", "fct_orgs": [],
     'enabled': True},
]

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

# extra suffixes while using 'meetingadvicefinances_workflow'
FINANCE_GROUP_SUFFIXES = ('financialcontrollers',
                          'financialeditors',
                          'financialreviewers',
                          'financialmanagers')
FINANCE_STATE_TO_GROUPS_MAPPINGS = {
    'proposed_to_financial_controller': 'financialcontrollers',
    'proposed_to_financial_editor': 'financialeditors',
    'proposed_to_financial_reviewer': 'financialreviewers',
    'proposed_to_financial_manager': 'financialmanagers', }

# states in which the finance advice may be given
FINANCE_WAITING_ADVICES_STATES = ['prevalidated_waiting_advices']

# the id of the collection querying finance advices
FINANCE_ADVICES_COLLECTION_ID = 'searchitemswithfinanceadvice'

# if True, a positive finances advice may be signed by a finances reviewer
# if not, only the finances manager may sign advices
POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER = False

# text about FD advice used in templates
FINANCE_ADVICE_LEGAL_TEXT_PRE = "<p>Attendu la demande d'avis adressée sur " \
                                "base d'un dossier complet au Directeur financier en date du {0};<br/></p>"

FINANCE_ADVICE_LEGAL_TEXT = "<p>Attendu l'avis {0} du Directeur financier " \
                            "rendu en date du {1} conformément à l'article L1124-40 du Code de la " \
                            "démocratie locale et de la décentralisation;</p>"

FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN = "<p>Attendu l'absence d'avis du " \
                                      "Directeur financier rendu dans le délai prescrit à l'article L1124-40 " \
                                      "du Code de la démocratie locale et de la décentralisation;</p>"

STYLESHEETS = [{'id': 'MeetingMons.css',
                'title': 'MeetingMons CSS styles'}]
