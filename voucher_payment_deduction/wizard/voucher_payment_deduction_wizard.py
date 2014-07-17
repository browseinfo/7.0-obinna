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

class voucher_payment_deduction_wizard(osv.osv_memory):
    _name ='voucher.payment.deduction.wizard'
    
    def onchange_deduction(self, cr, uid, ids, deduction , context=None):
        vals = {}
        hr_salary_rule_value = self.pool.get('hr.salary.rule').browse(cr, uid, deduction , context=context)
        vals = {
            'head':hr_salary_rule_value.head,
            's_head':hr_salary_rule_value.sub_head,
            'classification_code':hr_salary_rule_value.classification_code,
            'vo1':hr_salary_rule_value.vo1
        }
        return {'value': vals}
        
    def _get_code(self, cr, uid, context=None):
        categ_id = self.pool.get('hr.salary.rule.category').search(cr, uid, [('code','=','DED')], context=context)
        return categ_id and categ_id[0] or False
        
    _columns = {
         'period_id': fields.many2one('account.period', 'Period',  required=True),
         'bank_ids': fields.many2many('res.bank', 'employee_bank_rel_vou', 'bank_id', 'employee_id', 'Banks'),
         'code': fields.many2one('hr.salary.rule.category','code', required=True),
         'deduction': fields.many2one('hr.salary.rule','Deduction', required=True),
         'head':fields.char('Head'),
         's_head':fields.char('S/Head'),
         'department_no':fields.integer('Department No',size=50),
         'vo1':fields.char("VO1",size=12),
         'classification_code':fields.char("Classification Code",size=14),
         'payee':fields.char("Payee",size=100),
         'address':fields.text("Address")         
         }
         
    _defaults = {
         'code': _get_code,
         }    

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        datas = {
             'ids': [data.get('id')],
             'model': 'voucher.payment.deduction.wizard',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'voucher.deduction.report',
            'datas': datas,
        }

voucher_payment_deduction_wizard()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
