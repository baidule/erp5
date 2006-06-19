##############################################################################
#
# Copyright (c) 2004 Nexedi SARL and Contributors. All Rights Reserved.
#          Sebastien Robin <seb@nexedi.com>
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



#
# Skeleton ZopeTestCase
#

from random import randint

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

# Needed in order to have a log file inside the current folder
os.environ['EVENT_LOG_FILE'] = os.path.join(os.getcwd(), 'zLOG.log')
os.environ['EVENT_LOG_SEVERITY'] = '-300'

from Testing import ZopeTestCase
from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from DateTime import DateTime
from Acquisition import aq_base, aq_inner
from zLOG import LOG
from Products.ERP5Type.DateUtils import addToDate
import time
import os
from Products.ERP5Type import product_path
from DateTime import DateTime

class TestAlarm(ERP5TypeTestCase):
  """
  This is the list of test

  test setNextStartDate :
  - every hour
  - at 6, 10, 15, 21 every day
  - every day at 10
  - every 3 days at 14 and 15 and 17
  - every monday and friday, at 6 and 15
  - every 1st and 15th every month, at 12 and 14
  - every 1st day of every 2 month, at 6
  """

  # Different variables used for this test
  run_all_test = 1
  source_company_id = 'Nexedi'
  destination_company_id = 'Coramy'
  component_id = 'brick'
  sales_order_id = '1'
  quantity = 10
  base_price = 0.7832

  def getTitle(self):
    return "Alarm"

  def test_01_HasEverything(self, quiet=0, run=run_all_test):
    # Test if portal_synchronizations was created
    if not run: return
    if not quiet:
      ZopeTestCase._print('\nTest Has Everything ')
      LOG('Testing... ',0,'testHasEverything')
    self.failUnless(self.getCategoryTool()!=None)
    self.failUnless(self.getSimulationTool()!=None)
    self.failUnless(self.getTypeTool()!=None)
    self.failUnless(self.getSqlConnection()!=None)
    self.failUnless(self.getCatalogTool()!=None)

  #def populate(self, quiet=1, run=1):
  def afterSetUp(self, quiet=1, run=1):
    self.login()
    portal = self.getPortal()
    catalog_tool = self.getCatalogTool()
    # XXX This does not works
    #catalog_tool.reindexObject(portal)

    # First reindex
    #LOG('afterSetup',0,'portal.portal_categories.immediateReindexObject')
    #portal.portal_categories.immediateReindexObject()
    #LOG('afterSetup',0,'portal.portal_simulation.immediateReindexObject')
    #portal.portal_simulation.immediateReindexObject()

  def newAlarm(self):
    """
    Create an empty alarm
    """
    a_tool = self.getAlarmTool()
    return a_tool.newContent()

  def login(self, quiet=0, run=run_all_test):
    uf = self.getPortal().acl_users
    uf._doAddUser('seb', '', ['Manager'], [])
    user = uf.getUserById('seb').__of__(uf)
    newSecurityManager(None, user)

  def test_02_Initialization(self, quiet=0, run=run_all_test):
    """
    Test some basic things right after the creation
    """
    if not run: return
    if not quiet:
      message = 'Test Initialization'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    alarm = self.newAlarm()
    now = DateTime()
    date = addToDate(now,day=1)
    alarm.setPeriodicityStartDate(date)
    self.assertEquals(alarm.getAlarmDate(),date)
    alarm.setNextAlarmDate(current_date=now) # This should not do change the alarm date
    self.assertEquals(alarm.getAlarmDate(),date)

  def test_03_EveryHour(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Test Every Hour'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    alarm = self.newAlarm()
    now = DateTime()
    date = addToDate(now,day=2)
    alarm.setPeriodicityStartDate(date)
    alarm.setPeriodicityHourFrequency(1)
    alarm.setNextAlarmDate(current_date=now)
    self.assertEquals(alarm.getAlarmDate(),date)
    LOG(message + ' now :',0,now)
    now = addToDate(now,day=2)
    LOG(message + ' now :',0,now)
    alarm.setNextAlarmDate(current_date=now)
    next_date = addToDate(date,hour=1)
    self.assertEquals(alarm.getAlarmDate(),next_date)
    now = addToDate(now,hour=1,minute=5)
    alarm.setNextAlarmDate(current_date=now)
    next_date = addToDate(next_date,hour=1)
    self.assertEquals(alarm.getAlarmDate(),next_date)

  def test_04_Every3Hours(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Test Every 3 Hours'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    alarm = self.newAlarm()
    now = DateTime()
    hour_to_remove = now.hour() % 3
    now = addToDate(now,hour=-hour_to_remove)
    date = addToDate(now,day=2)
    alarm.setPeriodicityStartDate(date)
    alarm.setPeriodicityHourFrequency(3)
    alarm.setNextAlarmDate(current_date=now)
    self.assertEquals(alarm.getAlarmDate(),date)
    LOG(message + ' now :',0,now)
    now = addToDate(now,day=2)
    LOG(message + ' now :',0,now)
    alarm.setNextAlarmDate(current_date=now)
    next_date = addToDate(date,hour=3)
    self.assertEquals(alarm.getAlarmDate(),next_date)
    now = addToDate(now,hour=3,minute=7,second=4)
    alarm.setNextAlarmDate(current_date=now)
    next_date = addToDate(next_date,hour=3)
    self.assertEquals(alarm.getAlarmDate(),next_date)

  def test_05_SomeHours(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Test Some Hours'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,15,00,00))
    now = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,15,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,21,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,7,06,00,00))
    right_fourth_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,7,10,00,00))
    alarm = self.newAlarm()
    hour_list = (6,10,15,21)
    alarm.setPeriodicityStartDate(now)
    alarm.setPeriodicityHourList(hour_list)
    self.assertEquals(alarm.getAlarmDate(),right_first_date)
    alarm.setNextAlarmDate(current_date=right_first_date)
    self.assertEquals(alarm.getAlarmDate(),right_second_date)
    alarm.setNextAlarmDate(current_date=right_second_date)
    self.assertEquals(alarm.getAlarmDate(),right_third_date)
    alarm.setNextAlarmDate(current_date=right_third_date)
    self.assertEquals(alarm.getAlarmDate(),right_fourth_date)

  def test_06_EveryDayOnce(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Every Day Once'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    now = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,10,00,00))
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,10,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,7,10,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,8,10,00,00))
    alarm = self.newAlarm()
    alarm.setPeriodicityStartDate(now)
    alarm.setPeriodicityDayFrequency(1)
    alarm.setPeriodicityHourList((10,))
    self.assertEquals(alarm.getAlarmDate(),right_first_date)
    alarm.setNextAlarmDate(current_date=right_first_date)
    self.assertEquals(alarm.getAlarmDate(),right_second_date)
    alarm.setNextAlarmDate(current_date=right_second_date)
    self.assertEquals(alarm.getAlarmDate(),right_third_date)

  def test_07_Every3DaysSomeHours(self, quiet=0, run=run_all_test):
    """- every 3 days at 14 and 15 and 17"""
    if not run: return
    if not quiet:
      message = 'Every 3 Days Some Hours'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,14,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,15,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,6,17,00,00))
    right_fourth_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,9,14,00,00))
    alarm = self.newAlarm()
    alarm.setPeriodicityStartDate(right_first_date)
    alarm.setPeriodicityDayFrequency(3)
    alarm.setPeriodicityHourList((14,15,17))
    self.assertEquals(alarm.getAlarmDate(),right_first_date)
    alarm.setNextAlarmDate(current_date=right_first_date)
    self.assertEquals(alarm.getAlarmDate(),right_second_date)
    alarm.setNextAlarmDate(current_date=right_second_date)
    self.assertEquals(alarm.getAlarmDate(),right_third_date)
    alarm.setNextAlarmDate(current_date=right_third_date)
    self.assertEquals(alarm.getAlarmDate(),right_fourth_date)

  def test_08_SomeWeekDaysSomeHours(self, quiet=0, run=run_all_test):
    """- every monday and friday, at 6 and 15"""
    if not run: return
    if not quiet:
      message = 'Some Week Days Some Hours'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,9,27,6,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,9,27,15,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,1,6,00,00))
    right_fourth_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,1,15,00,00))
    alarm = self.newAlarm()
    alarm.setPeriodicityStartDate(right_first_date)
    alarm.setPeriodicityWeekDayList(('Monday','Friday'))
    alarm.setPeriodicityHourList((6,15))
    self.checkDate(alarm, right_first_date, right_second_date, right_third_date, right_fourth_date)
    #self.assertEquals(alarm.getAlarmDate(),right_first_date)
    #alarm.setNextAlarmDate(current_date=right_first_date)
    #self.assertEquals(alarm.getAlarmDate(),right_second_date)
    #alarm.setNextAlarmDate(current_date=right_second_date)
    #self.assertEquals(alarm.getAlarmDate(),right_third_date)
    #alarm.setNextAlarmDate(current_date=right_third_date)
    #self.assertEquals(alarm.getAlarmDate(),right_fourth_date)


  def checkDate(self,alarm,*args):
    """
    the basic test
    """
    for date in args[:-1]:
      LOG('checkDate, checking date...:',0,date)
      self.assertEquals(alarm.getAlarmDate(),date)
      alarm.setNextAlarmDate(current_date=date)
    self.assertEquals(alarm.getAlarmDate(),args[-1])

  def test_09_SomeMonthDaysSomeHours(self, quiet=0, run=run_all_test):
    """- every 1st and 15th every month, at 12 and 14"""
    if not run: return
    if not quiet:
      message = 'Some Month Days Some Hours'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,01,12,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,01,14,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,15,12,00,00))
    right_fourth_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,15,14,00,00))
    alarm = self.newAlarm()
    alarm.setPeriodicityStartDate(right_first_date)
    alarm.setPeriodicityMonthDayList((1,15))
    alarm.setPeriodicityHourList((12,14))
    self.checkDate(alarm, right_first_date, right_second_date, right_third_date, right_fourth_date)

  def test_10_OnceEvery2Month(self, quiet=0, run=run_all_test):
    """- every 1st day of every 2 month, at 6"""
    if not run: return
    if not quiet:
      message = 'Once Every 2 Month'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,01,6,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,12,01,6,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2005,2,01,6,00,00))
    alarm = self.newAlarm()
    alarm.setPeriodicityStartDate(right_first_date)
    alarm.setPeriodicityMonthDayList((1,))
    alarm.setPeriodicityMonthFrequency(2)
    alarm.setPeriodicityHourList((6,))
    self.checkDate(alarm, right_first_date, right_second_date, right_third_date)

  def test_11_EveryDayOnceWeek41And42(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Every Day Once Week 41 And 43'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    # year/month/day hour:minute:second
    right_first_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,10,6,00,00))
    right_second_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,18,6,00,00))
    right_third_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,19,6,00,00))
    right_fourth_date = DateTime('%i/%i/%i %i:%i:%d' % (2004,10,20,6,00,00))
    alarm = self.newAlarm()
    alarm.setPeriodicityStartDate(right_first_date)
    alarm.setPeriodicityHourList((6,))
    alarm.setPeriodicityWeekList((41,43))
    self.checkDate(alarm, right_first_date, right_second_date, right_third_date,right_fourth_date)

  def test_12_Every5Minutes(self, quiet=0, run=run_all_test):
    if not run: return
    if not quiet:
      message = 'Test Every 5 Minutes'
      ZopeTestCase._print('\n%s ' % message)
      LOG('Testing... ',0,message)
    alarm = self.newAlarm()
    now = DateTime()
    minute_to_remove = now.minute() % 5
    now = addToDate(now,minute=-minute_to_remove)
    date = addToDate(now,day=2)
    alarm.setPeriodicityStartDate(date)
    alarm.setPeriodicityMinuteFrequency(5)
    alarm.setNextAlarmDate(current_date=now)
    self.assertEquals(alarm.getAlarmDate(),date)
    LOG(message + ' now :',0,now)
    now = addToDate(now,day=2)
    LOG(message + ' now :',0,now)
    alarm.setNextAlarmDate(current_date=now)
    next_date = addToDate(date,minute=5)
    self.assertEquals(alarm.getAlarmDate(),next_date)
    now = addToDate(now,minute=5,second=14)
    alarm.setNextAlarmDate(current_date=now)
    next_date = addToDate(next_date,minute=5)
    self.assertEquals(alarm.getAlarmDate(),next_date)

if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestAlarm))
        return suite

