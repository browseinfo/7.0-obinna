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

class advance_deduction_wizard(osv.osv_memory):
    _name ='advance.deduction.wizard'

    def _get_code(self, cr, uid, context=None):
        categ_id = self.pool.get('hr.salary.rule.category').search(cr, uid, [('code','=','DED')], context=context)
        return categ_id and categ_id[0] or False

    _columns = {
         'period_id': fields.many2one('account.period', 'Period',  required=True),
         'bank_ids': fields.many2many('res.bank', 'employee_bank_rel_ded', 'bank_id', 'employee_id', 'Banks'),
         #'payroll_no': fields.char('Payroll No', required=True),
         'code': fields.many2one('hr.salary.rule.category','code', required=True),
         'deduction': fields.many2one('hr.salary.rule','Deduction', required=True),
         'head':fields.char('Head'),
         's_head':fields.char('S/Head'),
         }
    
    _defaults = {
         'code': _get_code,
         }

    def print_advice_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
         
        datas = {
             'ids': [data.get('id')],
             'model': 'advance.deduction.wizard',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'advice.deduct',
            'datas': datas,
        }

advance_deduction_wizard()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
