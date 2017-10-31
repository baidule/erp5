"""Create Dataset for basic Trial Balance Report such as defined at
https://lab.nexedi.com/nexedi/erp5/blob/master/product/ERP5/tests/testAccountingReports.py#L4583

The test operates on 'today' transactions.

:param with_ledger: if true then data are prepared for 
    testOtherPartiesReportLedger unittest rather than testOtherPartiesReport
"""

from DateTime import DateTime

portal = context.getPortalObject()
accounting_module = portal.accounting_module
account_module = portal.account_module
ledger = portal.portal_categories.ledger
organisation_module = portal.organisation_module
person_module = portal.person_module

one_hour = 1.0 / 24.0
now = DateTime()
today = DateTime(now.year(), now.month(), now.day()) + 8 * one_hour

if with_ledger:
    extra_kwargs_general = {'ledger': 'accounting/general'}
    extra_kwargs_detailed = {'ledger': 'accounting/detailed'}

    accounting_ledger = ledger.get('accounting', None) \
        or ledger.newContent(portal_type='Category', id='accounting')

    if accounting_ledger.get('general', None) is None:
        accounting_ledger.newContent(portal_type='Category', id='general')
    if accounting_ledger.get('detailed', None) is None:
        accounting_ledger.newContent(portal_type='Category', id='detailed')

    # necessary for the "ledger" form field to appear and have correct options
    accounting_transaction = portal.portal_types.get('Accounting Transaction')
    if not accounting_transaction.getLedgerList():
        accounting_transaction.setProperty(
            "ledger_list", ['accounting/general', 'accounting/detailed'])
else:
    extra_kwargs_general = {}
    extra_kwargs_detailed = {}

context.AccountingZuite_createDocument(
    portal_type='Accounting Transaction',
    title='Transaction 1',
    source_reference='1',
    simulation_state='delivered',
    destination_section_value=organisation_module.client_1,
    start_date=today + 1 * one_hour,
    embedded=(dict(portal_type='Accounting Transaction Line',
              source_value=account_module.receivable,
              source_debit=100.0),
              dict(portal_type='Accounting Transaction Line',
              source_value=account_module.goods_sales,
              source_credit=100.0)),
    **extra_kwargs_general
    )

context.AccountingZuite_createDocument(
    portal_type='Accounting Transaction',
    title='Transaction 2',
    source_reference='2',
    simulation_state='delivered',
    destination_section_value=organisation_module.client_1,
    start_date=today + 2 * one_hour,
    embedded=(dict(portal_type='Accounting Transaction Line',
              source_value=account_module.payable, source_debit=200.0),
              dict(portal_type='Accounting Transaction Line',
              source_value=account_module.goods_sales,
              source_credit=200.0)),
    **extra_kwargs_general
    )

if with_ledger:
    context.AccountingZuite_createDocument(
        portal_type='Accounting Transaction',
        title='Transaction 3',
        source_reference='3',
        simulation_state='delivered',
        destination_section_value=organisation_module.client_1,
        start_date=today + 3 * one_hour,
        embedded=(dict(portal_type='Accounting Transaction Line',
                  source_value=account_module.payable, source_debit=400.0),
                  dict(portal_type='Accounting Transaction Line',
                  source_value=account_module.goods_sales,
                  source_credit=400.0)),
        **extra_kwargs_detailed
        )
