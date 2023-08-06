# -*- coding: utf-8 -*-
#
# File: testWorkflows.py
#
# Copyright (c) 2007-2012 by CommunesPlone.org
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from AccessControl import Unauthorized
from zope.annotation import IAnnotations
from Products.CMFCore.permissions import View
from Products.MeetingMons.tests.MeetingMonsTestCase import MeetingMonsTestCase
from Products.MeetingCommunes.tests.testWorkflows import testWorkflows as mctw
from Products.PloneMeeting.utils import get_annexes


class testWorkflows(MeetingMonsTestCase, mctw):
    """Tests the default workflows implemented in MeetingMons."""

    def test_pm_WholeDecisionProcess(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
            This call 2 sub tests for each process : college and council
        """
        self._testWholeDecisionProcessCollege()
        self._testWholeDecisionProcessCouncil()

    def _testWholeDecisionProcessCollege(self):
        '''This test covers the whole decision workflow. It begins with the
           creation of some items, and ends by closing a meeting.'''
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        self.addAnnex(item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.proposeItem(item1)
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        self.proposeItem(item2)
        # pmReviewer1 validates item1 and adds an annex to it
        self.changeUser('pmReviewer1')
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'validate')
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item1))
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.addAnnex(item1, relatedTo='item_decision')
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        self.addAnnex(item1, relatedTo='item_decision')
        # Now reviewers can't add annexes anymore
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item2)
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        # meeting is frozen
        self.changeUser('pmManager')
        self.do(meeting, 'freeze')
        self.addAnnex(item1, relatedTo='item_decision')
        # pmReviewer2 validates item2
        self.changeUser('pmReviewer2')
        self.do(item2, 'validate')
        # pmManager inserts item2 into the meeting, as late item, and adds an
        # annex to it
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # So now we should have 3 normal item (2 recurring + 1) and one late item in the meeting
        self.failUnless(len(meeting.getItems()) == 4)
        self.failUnless(len(meeting.getItems(listTypes='late')) == 1)
        self.changeUser('pmManager')
        item1.setDecision(self.decisionText)

        # pmManager adds a decision for item2, and decides both meeting and item
        self.changeUser('pmManager')
        item2.setDecision(self.decisionText)
        self.addAnnex(item2, relatedTo='item_decision')
        self.do(meeting, 'decide')
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'accept')
        self.changeUser('pmCreator1')
        self.addAnnex(item1, relatedTo='item_decision')
        self.changeUser('pmServiceHead1')
        self.addAnnex(item1, relatedTo='item_decision')
        self.changeUser('pmOfficeManager1')
        self.addAnnex(item1, relatedTo='item_decision')
        self.changeUser('pmDivisionHead1')
        self.addAnnex(item1, relatedTo='item_decision')
        self.changeUser('pmDirector1')
        self.addAnnex(item1, relatedTo='item_decision')

        # pmCreator2/pmReviewer2 are not able to see item1
        self.changeUser('pmCreator2')
        self.failIf(self.hasPermission(View, item1))
        self.changeUser('pmReviewer2')
        self.failIf(self.hasPermission(View, item1))

        # meeting may be closed or set back to frozen
        self.changeUser('pmManager')
        self.assertEquals(self.transitions(meeting), ['backToFrozen', 'close'])
        self.changeUser('pmManager')
        self.do(meeting, 'close')
        self.addAnnex(item1, relatedTo='item_decision')

    def _testWholeDecisionProcessCouncil(self):
        """
            This test covers the whole decision workflow. It begins with the
            creation of some items, and ends by closing a meeting.
        """
        # meeting-config-college is tested in test_pm_WholeDecisionProcessCollege
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        # pmCreator1 creates an item with 1 annex and proposes it
        self.changeUser('pmCreator1')
        item1 = self.create('MeetingItem', title='The first item')
        self.addAnnex(item1)
        # The creator can add a decision annex on created item
        self.addAnnex(item1, relatedTo='item_decision')
        self.proposeItem(item1)
        # The creator cannot add a decision annex on proposed item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.failIf(self.transitions(item1))  # He may trigger no more action
        # pmManager creates a meeting
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2007/12/11 09:00:00')
        # The meetingManager can add a decision annex
        self.addAnnex(item1, relatedTo='item_decision')
        # pmCreator2 creates and proposes an item
        self.changeUser('pmCreator2')
        item2 = self.create('MeetingItem', title='The second item',
                            preferredMeeting=meeting.UID())
        self.proposeItem(item2)
        # pmReviewer1 validates item1 and adds an annex to it
        self.changeUser('pmReviewer1')
        # The reviewer can add a decision annex on proposed item
        self.addAnnex(item1, relatedTo='item_decision')
        self.do(item1, 'validate')
        # The reviewer cannot add a decision annex on validated item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        # pmManager inserts item1 into the meeting and freezes it
        self.changeUser('pmManager')
        managerAnnex = self.addAnnex(item1)
        self.portal.restrictedTraverse('@@delete_givenuid')(managerAnnex.UID())
        self.do(item1, 'present')
        self.changeUser('pmCreator1')
        # The creator cannot add any kind of annex on presented item
        self.assertRaises(Unauthorized, self.addAnnex, item1, relatedTo='item_decision')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.changeUser('pmManager')
        self.do(meeting, 'freeze')
        # pmReviewer2 validates item2
        self.changeUser('pmReviewer2')
        self.do(item2, 'validate')
        # pmManager inserts item2 into the meeting, as late item, and adds an
        # annex to it
        self.changeUser('pmManager')
        self.do(item2, 'present')
        self.addAnnex(item2)
        # So now I should have 1 normal item left and one late item in the meeting
        self.failIf(len(meeting.getItems()) != 2)
        self.failUnless(len(meeting.getItems(listTypes=['late'])) == 1)
        # pmReviewer1 can not add an annex on item1 as it is frozen
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item1)
        self.changeUser('pmManager')
        item1.setDecision(self.decisionText)
        # Now reviewers can't add annexes anymore
        self.changeUser('pmReviewer2')
        self.failIf(self.hasPermission('PloneMeeting: Add annex', item2))
        self.assertRaises(Unauthorized, self.addAnnex, item2, relatedTo='item_decision')
        self.changeUser('pmReviewer1')
        self.assertRaises(Unauthorized, self.addAnnex, item2)
        self.assertRaises(Unauthorized, self.addAnnex, item2, relatedTo='item_decision')
        # pmManager adds a decision for item2, decides and closes the meeting
        self.changeUser('pmManager')
        item2.setDecision(self.decisionText)
        self.do(meeting, 'decide')
        # check that a delayed item is duplicated
        self.assertEquals(len(item1.getBRefs('ItemPredecessor')), 0)
        self.do(item1, 'delay')
        # the duplicated item has item3 as predecessor
        duplicatedItem = item1.getBRefs('ItemPredecessor')[0]
        self.assertEquals(duplicatedItem.getPredecessor().UID(), item1.UID())
        # when duplicated on delay, annexes are kept
        self.assertEquals(len(get_annexes(duplicatedItem, portal_types=('annex', ))), 1)
        self.addAnnex(item2, relatedTo='item_decision')
        self.failIf(len(self.transitions(meeting)) != 2)
        # When a meeting is closed, items without a decision are automatically 'accepted'
        self.do(meeting, 'close')
        self.assertEquals(item2.queryState(), 'accepted')
        # An already decided item keep his given decision
        self.assertEquals(item1.queryState(), 'delayed')
        # XXX added tests regarding ticket #5887
        # test back transitions
        self.changeUser('admin')
        self.do(meeting, 'backToDecided')
        self.changeUser('pmManager')
        self.do(meeting, 'backToFrozen')
        # this also test the 'doBackToCreated' action on the meeting
        self.do(meeting, 'backToCreated')
        self.do(meeting, 'freeze')
        self.do(meeting, 'decide')
        self.do(meeting, 'close')

    def test_pm_WorkflowPermissions(self):
        """
          Pass this test...
        """
        pass

    def test_pm_RemoveContainer(self):
        '''Run the test_pm_RemoveContainer from PloneMeeting.'''
        # we do the test for the college config
        self.meetingConfig = getattr(self.tool, 'meeting-config-college')
        super(testWorkflows, self).test_pm_RemoveContainer()
        # we do the test for the council config
        self.meetingConfig = getattr(self.tool, 'meeting-config-council')
        # clean memoize because we test for status messages
        annotations = IAnnotations(self.portal.REQUEST)
        if 'statusmessages' in annotations:
            annotations['statusmessages'] = ''
        super(testWorkflows, self).test_pm_RemoveContainer()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflows, prefix='test_pm_'))
    return suite
