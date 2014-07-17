# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import time
from datetime import datetime
from dateutil import relativedelta

from osv import fields, osv

class bank_wizard(osv.osv_memory):
    _name ='bank.wizard'

    _columns = {
         'payment_code': fields.char('Payment Code', required=True),
         'period_id': fields.many2one('account.period', 'Period',  required=True),
         'bank_ids': fields.many2many('res.bank', 'employee_bank_rel', 'bank_id', 'employee_id', 'Banks'),
         'account_type': fields.boolean('Account Type'),
         'acc_unit': fields.boolean('BENEFICIARY ACCOAREA 11UNT'),
         'employee_one': fields.many2one('hr.employee', 'Employee One'),
         'employee_two': fields.many2one('hr.employee', 'Employee Two'),
    }

    def print_report(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
             'ids': [data.get('id')],
             'model': 'hr.payslip',
             'form': data
        }
        if data['acc_unit'] and data['account_type'] == False:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'payroll.bank.all.acc.unit',
                'datas': datas,
            }
        elif data['account_type'] and data['acc_unit'] == False:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'payroll.bank.all.account.type',
                'datas': datas,
            }
        elif data['acc_unit'] and data['account_type']:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'payroll.bank.all',
                'datas': datas,
            }
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'payroll.bank.all.without.type.unit',
                'datas': datas,
            }
            

bank_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
