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


class bank_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bank_report, self).__init__(cr, uid, name, context)
        self.counter = 0
        self.emp_one_name = ''
        self.emp_two_name = ''
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'sum_total': self._sum_total,
            'amount_word': self._amount_word,
            'call_date_from': self._call_date_from,
            'call_date_to': self._call_date_to,
            'get_bank_name': self._get_bank_name,
            'get_purpose': self._get_purpose,
            'get_emp_name_one': self._get_emp_name_one,
            'get_emp_name_two': self._get_emp_name_two,
        })
        
    def _call_date_from(self, obj):
        date = datetime.strptime(self.date_from, '%Y-%m-%d')
        return (str(date.day) + '/' + str(date.month) + '/' + str(date.year))
        
    def _call_date_to(self, obj):
        date = datetime.strptime(self.date_to, '%Y-%m-%d')
        return (str(date.day) + '/' + str(date.month) + '/' + str(date.year))
        
    def _sum_total(self):
        return self.total
    
    def _get_emp_name_one(self):
        return self.emp_one_name
        
    def _get_emp_name_two(self):
        return self.emp_two_name
                
    def _get_purpose(self, obj):
        date = datetime.strptime(self.date_to, '%Y-%m-%d').strftime('%b-%Y')
        return (str(date) + ' Salary')
        
    def _amount_word(self):
        amount = amount_to_text(self.total)
        word = str(amount) + ' Only'
        return word
        
    def _get_bank_name(self, obj,):
        self.cr.execute("select name from res_bank where id = %s", (obj.bank_ids[0].id,))
        name = str(self.cr.fetchone())
        if "(u'" in name:
            if " - " in name:
                name = name.split(" - ")
                return name[0].split("u'")[1]
            else:
                name = name.split("(u")
                name = name[1].split("',)")
                name = name[0].split("'")
                return name[1]
            
        
    def set_context(self, objects, data, ids, report_type=None):
        employee_obj = self.pool.get('hr.employee')
        period_obj = self.pool.get('account.period')
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['period_id'][1] )])
        if data['form']['employee_one']:
            self.emp_one_name = data['form']['employee_one'][1]
        if data['form']['employee_two']:
            self.emp_two_name = data['form']['employee_two'][1]
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['period_id'][1] )])
        for period in period_obj.browse(self.cr, self.uid, period_id):
            self.date_from = period.date_start
            self.date_to = period.date_stop
        return super(bank_report, self).set_context(objects, data, ids, report_type=report_type)
        
    def _get_payslip_lines(self, obj, column_flag=0):
        bank_wizard_obj = self.pool.get('bank.wizard')
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        
        self.total = 0.0
        self.bank = obj.bank_ids 
        self.payment_code = obj.payment_code
        city = ''
        street = ''
        
        for bank in obj.bank_ids:
            self.cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (bank.id,))
            
            bank_ids = [x[0] for x in self.cr.fetchall()]
            line_name = []
            for bank_id in bank_ids:
                self.cr.execute("select hps.id from hr_payslip_line hp "\
                        "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                        "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                        "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                        "AND he.bank_name = %s order by hp.amount", (self.date_from, self.date_to, bank_id,))
                temp = self.cr.fetchone()
                if temp:
                    line_name.append(temp[0])
            
            for line in payslip_line.browse(self.cr, self.uid, line_name):
                computation_lines = {}
                wages = {}
                self.counter = self.counter + 1
                if line.employee_id.rank_id.grade_id:
                    grade_name = line.employee_id.rank_id.grade_id.name
                if line.employee_id.rank_id.step_id:
                    step_name = line.employee_id.rank_id.step_id.name
                
                for l in line.line_ids:
                    wages[l.name] = l.amount
                    
                if grade_name and step_name:
                    if grade_name == 'Secretary' and step_name == 'Member' or step_name == 'Secretary' and grade_name == 'Member':
                        allowance = (wages['Housing'] + wages['Transport'] + wages['Meal'] + wages['Utilities'] + wages['Furniture'] + wages['Domestic Staff'] + wages['Leave Grant'] + wages['Arrears'] + wages['Under Payment'] + wages['Peculiar Allowances'] + wages['Arrear Allowance'] + wages['Motor Maintainance and Fueling'] + wages['Entertainment'] + wages['Accomodation'] + wages['Personal Assistant'] + wages['Newspaper'])
                        total_allowance = {'total_allowance' : allowance}
                        wages.update(total_allowance)

                        deductions = (wages['Tax'] + wages['Rent'] + wages['Over Payment'] + wages['Pension'] + wages['NHF'] + wages['CTLS'] + wages['NHIS'] + wages['Salary Advance'] + wages['Motor Vehicle Advance'] + wages['FGHB'] + wages['Other Deduction'] + wages['Personal Advance'])
                        total_deductions = {'deductions': deductions}
                        wages.update(total_deductions)

                        total_basic_salary = wages['Basic'] + wages['Overtime'] + wages['Arrears']
                        total_basic_sal = {'total_basic_salary': total_basic_salary}
                        wages.update(total_basic_sal)

                        total_consolidated_salary = wages['Consolidated Allowance'] + wages['Overtime'] + wages['Arrears']
                        total_consolidated_sal = {'total_consolidated_salary': total_consolidated_salary}
                        wages.update(total_consolidated_sal)
                        
                        consolidated_alw = wages['total_basic_salary'] + wages['total_allowance']
                        consolidated = {'consolidated': consolidated_alw}
                        wages.update(consolidated)

                        emoluments = wages['consolidated'] - wages['deductions']
                        net_emolument = {'net_emoluments':emoluments}
                        wages.update(net_emolument)

                    else:
                        allowance = wages['Peculiar Allowances'] + wages['Arrear Allowance'] + wages['Under Payment']
                        total_allowance = {'total_allowance' : allowance}
                        wages.update(total_allowance)

                        deductions = (wages['Tax'] + wages['Rent'] + wages['Over Payment'] + wages['Pension'] + wages['NHF'] + wages['CTLS'] + wages['NHIS'] + wages['Salary Advance'] + wages['Motor Vehicle Advance'] + wages['FGHB'] + wages['Other Deduction'] + wages['Personal Advance'])
                        total_deductions = {'deductions': deductions}
                        wages.update(total_deductions)

                        total_basic_salary = wages['Basic'] + wages['Overtime'] + wages['Arrears']
                        total_basic_sal = {'total_basic_salary': total_basic_salary}
                        wages.update(total_basic_sal)

                        consolidated_salary = wages['Consolidated Allowance']
                        consolidated_sal = {'consolidated_salary': consolidated_salary}
                        wages.update(consolidated_sal)

                        total_consolidated_salary = wages['Consolidated Allowance'] + wages['Overtime'] + wages['Arrears']
                        total_consolidated_sal = {'total_consolidated_salary': total_consolidated_salary}
                        wages.update(total_consolidated_sal)     
                        
                        consolidated_alw = wages['total_allowance'] + wages['total_consolidated_salary']
                        consolidated = {'consolidated': consolidated_alw}
                        wages.update(consolidated)

                        emoluments = (wages['consolidated'] - wages['deductions'])
                        net_emolument = {'net_emoluments':emoluments}
                        wages.update(net_emolument) 
                                         
                    if line.employee_id.bank_name.street:
                        street = line.employee_id.bank_name.street
                            
                    if line.employee_id.bank_name.city:
                        city = line.employee_id.bank_name.city
                     
                    address =  street + ' ' + city
                    self.total += wages['net_emoluments']
                    res.append({
                                    'payment_code': self.payment_code or '',
                                    'computation': wages['net_emoluments'] or '',
                                    'employee_name': line.employee_id.name or '',
                                    'acc_number': line.employee_id.bank_name.acc_number or '',
                                    'account_name': line.employee_id.name or '',
                                    'branch_code': line.employee_id.bank_name.branch_code or '',
                                    'sort_code': line.employee_id.bank_name.sort_code or '',
                                    'bank_name': line.employee_id.bank_name.bank_name or '',
                                    'address': address or '',
                                    'purpose': line.name or '',
                                    'account_type': line.employee_id.bank_name.account_type or '',
                                    'acc_unit': line.employee_id.bank_name.acc_unit or '',
                                    'counter': self.counter,
                                    })
                                      
        return res

for suffix in ['', '.account.type', '.acc.unit', '.without.type.unit']:
    if suffix == '':
        report_sxw.report_sxw('report.payroll.bank.all' + suffix,
                              'hr.payslip', 
                              'addons/bank_report/report/bank_report.mako', 
                              parser=bank_report, 
                              header=False)
    elif suffix == '.account.type':
        report_sxw.report_sxw('report.payroll.bank.all' + suffix,
                              'hr.payslip', 
                              'addons/bank_report/report/bank_report_account_type.mako', 
                              parser=bank_report, 
                              header=False)
    elif suffix == '.acc.unit':
        report_sxw.report_sxw('report.payroll.bank.all' + suffix,
                              'hr.payslip', 
                              'addons/bank_report/report/bank_report_acc_unit.mako', 
                              parser=bank_report, 
                              header=False)
    elif suffix == '.without.type.unit':
        report_sxw.report_sxw('report.payroll.bank.all' + suffix,
                              'hr.payslip', 
                              'addons/bank_report/report/bank_report_all.mako', 
                              parser=bank_report, 
                              header=False)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
