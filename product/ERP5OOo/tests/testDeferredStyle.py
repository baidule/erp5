# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2009 Nexedi SA and Contributors. All Rights Reserved.
#          Nicolas Delaby <nicolas@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##############################################################################

import unittest
import transaction
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from Products.ERP5Form.Selection import Selection
from Testing import ZopeTestCase
from Products.ERP5Type.tests.utils import DummyMailHost
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Products.ERP5OOo.tests.utils import Validator
import email


class TestDeferredStyle(ERP5TypeTestCase, ZopeTestCase.Functional):
  """Tests deferred styles for ERP5."""
  skin = content_type = None
  recipient_email_address = 'invalid@example.com'
  username = 'bob'
  password = 'bobpwd'
  first_name = 'Bob'

  def getTitle(self):
    return 'Test Deferred Style'

  def getBusinessTemplateList(self):
    return ('erp5_base', 'erp5_ods_style',
            'erp5_odt_style', 'erp5_deferred_style',)

  def afterSetUp(self):
    self.login()
    if not self.skin:
      raise NotImplementedError('Subclasses must define skin')

    person_module = self.portal.person_module
    if person_module._getOb('pers', None) is None:
      person = person_module.newContent(id='pers', portal_type='Person',
                                        reference=self.username,
                                        first_name=self.first_name,
                                        password=self.password,
                                        default_email_text=self.recipient_email_address)
      assignment = person.newContent(portal_type='Assignment')
      assignment.open()

    # replace MailHost
    if 'MailHost' in self.portal.objectIds():
      self.portal.manage_delObjects(['MailHost'])
    self.portal._setObject('MailHost', DummyMailHost('MailHost'))
    transaction.commit()
    self.tic()

  def loginAsUser(self, username):
    uf = self.portal.acl_users
    uf.zodb_roles.assignRoleToPrincipal('Manager', username)
    user = uf.getUserById(username).__of__(uf)
    newSecurityManager(None, user)

  def test_skin_selection(self):
    self.assertTrue('Deferred' in self.portal.portal_skins.getSkinSelections())

  def test_report_view(self):
    self.loginAsUser('bob')
    self.portal.changeSkin('Deferred')
    response = self.publish(
        '/%s/person_module/pers/Base_viewHistory?deferred_portal_skin=%s'
        % (self.portal.getId(), self.skin), '%s:%s' % (self.username, self.password))
    transaction.commit()
    self.tic()
    last_message = self.portal.MailHost._last_message
    self.assertNotEquals((), last_message)
    mfrom, mto, message_text = last_message
    self.assertEquals('"%s" <%s>' % (self.first_name, self.recipient_email_address), mto[0])
    mail_message = email.message_from_string(message_text)
    for part in mail_message.walk():
      content_type = part.get_content_type()
      file_name = part.get_filename()
      # XXX the attachment name might change some day
      if file_name == 'report_view':
        self.assertEquals(content_type, self.content_type)
        data = part.get_payload(decode=True)
        error_list = Validator().validate(data)
        if error_list:
          self.fail(''.join(error_list))
        break
    else:
      self.fail('Attachment not found in email')


class TestODSDeferredStyle(TestDeferredStyle):
  skin = 'ODS'
  content_type = 'application/vnd.oasis.opendocument.spreadsheet'


class TestODTDeferredStyle(TestDeferredStyle):
  skin = 'ODT'
  content_type = 'application/vnd.oasis.opendocument.text'


def test_suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(TestODSDeferredStyle))
  suite.addTest(unittest.makeSuite(TestODTDeferredStyle))
  return suite

