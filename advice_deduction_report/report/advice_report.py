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
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from report import report_sxw
from openerp.tools.amount_to_text_en import amount_to_text


class advice_deduction(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(advice_deduction, self).__init__(cr, uid, name, context)
        self.amount_total = 0.0
        self.amount_n_total = 0.0
        self.bank_name =''
        self.localcontext.update({
             'get_payslip_lines': self._get_payslip_lines,
             'get_period': self._get_period,
             'get_deduction': self._get_deduction,
             'get_payroll': self._get_payroll,
             'get_total': self._get_total,
             'amount_word': self._amount_word,
             'get_n_total':self.get_n_total,
             'get_s_head':self.get_s_head,
             'get_bank_name':self.get_bank_name,
        })

    def set_context(self, objects, data, ids, report_type=None):
        #self.bank_name = bank_id.name
        self.wizard_period = data['form']['period_id'][0]
        self.date_period = self.pool.get('account.period').browse(self.cr, self.uid, self.wizard_period).date_start
        self.date_end = self.pool.get('account.period').browse(self.cr, self.uid, self.wizard_period).date_stop
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(self.date_period, formatter_string)
        date_object = datetime_object.date()
        self.period = date_object.strftime("%B %Y")
        #self.payroll = data['form']['payroll_no']
        self.deduction = data['form']['deduction'][1]
        self.category = data['form']['deduction'][0]
        return super(advice_deduction, self).set_context(objects, data, ids, report_type=report_type)

    def _get_total(self, obj):
        return self.amount_total

    def _amount_word(self):
        amount = amount_to_text(self.amount_total)
        word = str(amount) + ' Only'
        return word
    
    def get_s_head(self,data):
        return data['s_head']
    
    def get_bank_name(self,data):
        self.cr.execute("select name from res_bank where id = %s", (data,))
        rows = self.cr.fetchall()
        return rows[0][0]
    
    def _get_payslip_lines(self, obj, column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        self.amount_total = 0.0
        self.cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (obj,))
        bank_ids = [x[0] for x in self.cr.fetchall()]
        line_name = []
        for bank_id in bank_ids:
            self.cr.execute("select hps.id from hr_payslip_line hp "\
                    "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                    "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                    "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                    "AND hp.name = %s "\
                    "AND he.bank_name = %s order by hp.amount", (self.date_period, self.date_end, self.deduction, bank_id,))
            temp = self.cr.fetchone()
            if temp:
                line_name.append(temp[0])
        
        for line in payslip_line.browse(self.cr, self.uid, line_name):
            computation_lines = {}
            for l in line.line_ids:
                    computation_lines[l.name]= l.amount
            res.append({
                            'computation': computation_lines,
                            'employee' : line.employee_id.name,
                           })
        for i in res:     
            name = self.deduction           
            amount = i['computation'][name]
            result.append({
                           'amount': amount,
                           'employee': i['employee'],
                           })
            self.amount_total += amount
        return result
        
    def get_n_total(self, obj):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        self.amount_n_total = 0
        self.cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (obj,))
        bank_ids = [x[0] for x in self.cr.fetchall()]
        line_name = []
        for bank_id in bank_ids:
            self.cr.execute("select hps.id from hr_payslip_line hp "\
                    "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                    "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                    "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                    "AND hp.name = %s "\
                    "AND he.bank_name = %s order by hp.amount", (self.date_period, self.date_end, self.deduction, bank_id,))
            temp = self.cr.fetchone()
            if temp:
                line_name.append(temp[0])

        for line in payslip_line.browse(self.cr, self.uid, line_name):
            computation_lines = {}
            for l in line.line_ids:
                    computation_lines[l.name]= l.amount
            res.append({
                            'computation': computation_lines,
                            'employee' : line.employee_id.name,
                           })
        for i in res:     
            name = self.deduction           
            amount = i['computation'][name]
            result.append({
                           'amount': amount,
                           'employee': i['employee'],
                           })
            self.amount_n_total += amount
        return self.amount_n_total
    
    def _get_period(self):
        return self.period

    def _get_deduction(self, obj):
        return self.deduction

    def _get_payroll(self, obj):
        return self.payroll

report_sxw.report_sxw('report.advice.deduct', 'advance.deduction.wizard', 'advice_deduction_report/report/advice_report.rml', parser=advice_deduction, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
