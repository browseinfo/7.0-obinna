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


class pension_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(pension_report, self).__init__(cr, uid, name, context)
        self.count = 0
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'multikeysort' : self.multikeysort,
            'call_date_from': self._call_date_from,
            'call_date_to': self._call_date_to,
            'get_total': self._get_total,
            'get_seq': self._get_seq,
            
        })

    def _call_date_from(self, obj):
        date = datetime.strptime(self.date_from, '%Y-%m-%d')
        return (str(date.day) + '/' + str(date.month) + '/' + str(date.year))
        
    def _call_date_to(self, obj):
        date = datetime.strptime(self.date_to, '%Y-%m-%d')
        return (str(date.day) + '/' + str(date.month) + '/' + str(date.year))

    def set_context(self, objects, data, ids, report_type=None):
        period_obj = self.pool.get('account.period')
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['period_id'][1] )])
        for period in period_obj.browse(self.cr, self.uid, period_id):
            self.date_from = period.date_start
            self.date_to = period.date_stop
        return super(pension_report, self).set_context(objects, data, ids, report_type=report_type)
       
    def multikeysort(self,items, columns):
        from operator import itemgetter
        comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]  
        def comparer(left, right):
            for fn, mult in comparers:
                result = cmp(fn(left), fn(right))
                if result:
                    return mult * result
            else:
                return 0
        return sorted(items, cmp=comparer)
        
    def _get_total(self, obj,):
        result = []
        pension = 0.0
        for line in self.lines:
            pension += line['pension'] 
        result.append({
                'pension': pension,
                 })
                 
        return result
        
    def _get_seq(self):
        self.count += 1
        return self.count

    def _get_payslip_lines(self, obj, column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        line_name = []
        self.counter = 0
        
        self.cr.execute("select DISTINCT hps.id from hr_payslip_line hp "\
                "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                , (self.date_from, self.date_to,))
        
        payline_ids = [i[0] for i in self.cr.fetchall()]

        for line in payslip_line.browse(self.cr, self.uid, payline_ids):
            computation_lines = {}
            for l in line.line_ids:
                computation_lines[l.name]= l.amount
            if line.employee_id.rank_id:
                res.append({
                                'computation': computation_lines,
                                'employee' : line.employee_id.name,
                                'emp_id' : line.employee_id.id,
                                'rank_id': line.employee_id.rank_id.id,
                                'step_name': line.employee_id.rank_id.step_id.name,
                                'grade_id': line.employee_id.rank_id.grade_id.id,
                                'grade_name': line.employee_id.rank_id.grade_id.name,
                               })
        for i in res:
            self.amount_pension = 0.0
            payslip_ids = payslip_line .search(self.cr, self.uid, [('employee_id', '=',i['emp_id']),('date_from', '=',self.date_from),('date_to', '=',self.date_to)])
            

            if payslip_ids:
                for payslip in payslip_line.browse(self.cr, self.uid, payslip_ids):
                    for line in payslip.line_ids:
                        if line.name == 'Pension':
                            self.amount_pension = line.amount
            result.append({
            'name' :  i['employee'],   
            'pension' : self.amount_pension,
            'rank_id': i['rank_id'],
            'grade_id': i['grade_id'],
            'step_name': i['step_name'],
            'grade_name': i['grade_name'],
             })
             

        self.lines = result
        
        new_result = self.multikeysort(self.lines, ['-rank_id', 'name'])
        return new_result

report_sxw.report_sxw('report.pension.date.webkit.report', 'hr.payslip', 'addons/pension_webkit_report/report/pension_report.mako', parser=pension_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
