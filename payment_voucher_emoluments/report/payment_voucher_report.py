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
import calendar

class payment_voucher_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        self.total = 0
        super(payment_voucher_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'get_month':self._get_month,
            'amount_word': self._amount_word,
            'total':self._total,
            'get_bank':self._get_bank,
        })
    def _get_bank(self):
        return self.bank_name
        
    def set_context(self, objects, data, ids, report_type=None):
        period_obj = self.pool.get('account.period')
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['period_id'][1] )])
        self.bank_name = data['form']['bank_id'][1]
        for period in period_obj.browse(self.cr, self.uid, period_id):
            self.date_from = period.date_start
            self.date_to = period.date_stop
        return super(payment_voucher_report, self).set_context(objects, data, ids, report_type=report_type)
    def _get_payslip_lines(self, obj, column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        Gross = Entertainment = Over_Payment = Housing = Leave_Grant = Personal_Assistant = Basic = NHIS = Net = NHF = Newspaper_Allowance = Utilities = Personal_Advance = Furniture = Accomodation = CTLS = FGHB = Pension = Salary_Advance = Motor = Under = Domestic_Staff = Meal = Other_Deduction = Tax = Motor_Vehicle_Advance = Transport = RENT  = Peculiar = Acting_Allowance = Overtime = Mv_Adv_Including_Interest = 0.0
        self.bank = obj.bank_id.id
        
        self.cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (self.bank,))
        
        bank_ids = [x[0] for x in self.cr.fetchall()]
        line_name = []
        for bank_id in bank_ids:
            self.cr.execute("select hps.id from hr_payslip_line hp "\
                    "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                    "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                    "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                    "AND he.bank_name = %s", (self.date_from,self.date_to,bank_id,))
            temp = self.cr.fetchone()
            if temp:
                line_name.append(temp[0])
        
        computation_lines = {}
        for line in payslip_line.browse(self.cr, self.uid, line_name):
            for l in line.line_ids:
                computation_lines[l.name]= l.amount
                if l.name == 'Gross':
                    Gross += l.amount
                    computation_lines[l.name]= Gross
                if l.name == 'Entertainment':
                    Entertainment += l.amount
                    computation_lines[l.name] = Entertainment
                if l.name == 'Motor Maintainance and Fueling':
                    Motor += l.amount
                    computation_lines[l.name] = Motor
                if l.name == 'Under Payment':
                    Under += l.amount
                    computation_lines[l.name] = Under 
                if l.name == 'Peculiar Allowances':
                    Peculiar += l.amount
                    computation_lines[l.name] = Peculiar
                if l.name == 'Over Payment':
                    Over_Payment += l.amount
                    computation_lines[l.name] = Over_Payment
                if l.name == 'Housing':
                    Housing += l.amount
                    computation_lines[l.name] = Housing
                if l.name == 'Leave Grant':
                    Leave_Grant += l.amount
                    computation_lines[l.name] = Leave_Grant
                if l.name == 'Personal Assistant':
                    Personal_Assistant += l.amount
                    computation_lines[l.name] = Personal_Assistant
                if l.name == 'Basic':
                    Basic += l.amount
                    computation_lines[l.name] = Basic
                if l.name == 'NHIS':
                    NHIS += l.amount
                    computation_lines[l.name] = NHIS
                if l.name == 'Net':
                    Net += l.amount
                    computation_lines[l.name] = Net
                if l.name == 'NHF':
                    NHF += l.amount
                    computation_lines[l.name] = NHF
                if l.name == 'Newspaper':
                    Newspaper_Allowance += l.amount
                    computation_lines[l.name] = Newspaper_Allowance
                if l.name == 'Utilities':
                    Utilities += l.amount
                    computation_lines[l.name] = Utilities
                if l.name == 'Personal Advance':
                    Personal_Advance += l.amount
                    computation_lines[l.name] = Personal_Advance
                if l.name == 'Furniture':
                    Furniture += l.amount
                    computation_lines[l.name] = Furniture
                if l.name == 'Accomodation':
                    Accomodation += l.amount
                    computation_lines[l.name] = Accomodation
                if l.name == 'CTLS':
                    CTLS += l.amount
                    computation_lines[l.name] = CTLS
                if l.name == 'FGHB':
                    FGHB += l.amount
                    computation_lines[l.name] = FGHB
                if l.name == 'Pension':
                    Pension += l.amount
                    computation_lines[l.name] = Pension
                if l.name == 'Salary Advance':
                    Salary_Advance += l.amount
                    computation_lines[l.name] = Salary_Advance
                if l.name == 'Domestic Staff':
                    Domestic_Staff += l.amount
                    computation_lines[l.name] = Domestic_Staff
                if l.name == 'Meal':
                    Meal += l.amount
                    computation_lines[l.name] = Meal
                if l.name == 'Other Deduction':
                    Other_Deduction += l.amount
                    computation_lines[l.name] = Other_Deduction
                if l.name == 'Tax':
                    Tax += l.amount
                    computation_lines[l.name] = Tax
                if l.name == 'Motor Vehicle Advance':
                    Motor_Vehicle_Advance += l.amount
                    computation_lines[l.name] = Motor_Vehicle_Advance
                if l.name == 'Transport':
                    Transport += l.amount
                    computation_lines[l.name] = Transport
                if l.name == 'Rent':
                    RENT += l.amount
                    computation_lines[l.name] = RENT
                if l.name == 'Arrears':
                    Acting_Allowance += l.amount
                    computation_lines[l.name] = Acting_Allowance
                if l.name == 'Overtime':
                    Overtime += l.amount
                    computation_lines[l.name] = Overtime
                if l.name == 'Mv Adv Including Interest':
                    Mv_Adv_Including_Interest += l.amount
                    computation_lines[l.name] = Mv_Adv_Including_Interest
                    
        if computation_lines:
            grosss_amount = computation_lines['Basic'] + computation_lines['Arrears'] + computation_lines['Overtime']

            deducation_amount = computation_lines['Tax'] + computation_lines['NHF'] + computation_lines['Other Deduction'] + computation_lines['Pension']+ computation_lines['CTLS'] + computation_lines['NHIS'] + computation_lines['Mv Adv Including Interest'] +computation_lines['Personal Advance']+ computation_lines['Nigerian Region'] + computation_lines['FGHB'] + computation_lines['Over Payment'] + computation_lines['Salary Advance'] 
            
            deduct_voucher = deducation_amount
            
            taxble_1= computation_lines['Meal'] + computation_lines['Housing'] + computation_lines['Transport']+ computation_lines['Furniture'] + computation_lines['Arrears'] + computation_lines['Peculiar Allowances'] + computation_lines['Arrear Allowance'] + computation_lines['Newspaper'] + computation_lines['Motor Maintainance and Fueling']
            
            taxble_2= computation_lines['Entertainment'] + computation_lines['Utilities'] + computation_lines['Domestic Staff'] +computation_lines['Leave Grant'] + computation_lines['Under Payment'] + computation_lines['Accomodation'] + computation_lines['Personal Assistant']
    
            taxble = taxble_1 + taxble_2
            
            net_pay =  grosss_amount - deducation_amount
            self.total = taxble + net_pay
            result.append({
                'basic': computation_lines['Basic'], 
                'acting_allow': computation_lines['Arrears'],
                'overtime': computation_lines['Overtime'],
                'gross_amount': grosss_amount,
    
                'tax': computation_lines['Tax'],
                'nhf': computation_lines['NHF'],
                'other_ded': computation_lines['Other Deduction'],
                'pension': computation_lines['Pension'],
                'nhis': computation_lines['NHIS'],
                'ctls': computation_lines['CTLS'],
                'mv_adv_interest': computation_lines['Mv Adv Including Interest'],
                'personl_adv': computation_lines['Personal Advance'],
                'nigerin_reg': computation_lines['Nigerian Region'],
                'fghb': computation_lines['FGHB'],
                'over_payment': computation_lines['Over Payment'],
                'salary_advance': computation_lines['Salary Advance'],
                'deducation_amt': deducation_amount,
                'net_pay': net_pay,
                'meal': computation_lines['Meal'],
                'rent': computation_lines['Housing'],
                'transport':computation_lines['Transport'],  
                'furniture': computation_lines['Furniture'],
                'entertainment': computation_lines['Entertainment'],
                'utilities': computation_lines['Utilities'],
                'domestic_servent': computation_lines['Domestic Staff'],
                'leave_grant': computation_lines['Leave Grant'],
                'arrears': computation_lines['Arrear Allowance'],
                'under_payment': computation_lines['Under Payment'],
                'accomodation': computation_lines['Accomodation'],
                'personal_alw': computation_lines['Personal Assistant'],
                'motor_allw': computation_lines['Motor Maintainance and Fueling'],
                'newspaper': computation_lines['Newspaper'],
                'peculiar': computation_lines['Peculiar Allowances'],
                
                'taxable': taxble, 
                'net_total': taxble + net_pay,
                'motor_vehicle': computation_lines['Motor Vehicle Advance'],
                'deduct_voucher': deduct_voucher,
                #'name' :  computation_lines['employee'],   
                 })
        return result
        
    def _get_month(self, obj):
        month = int(obj.period_id.date_start.split('-')[1])
        return calendar.month_name[month]
    def _total(self):
        return self.total
    def _amount_word(self):
        amount = amount_to_text(self.total)
        word = str(amount) + ' Only'
        return word
report_sxw.report_sxw('report.payroll.summary.report', 'hr.payslip', 'addons/payment_voucher_emoluments/report/payment_voucher_report.mako', parser=payment_voucher_report, header="internal landscap")

class payment_voucher_report_consolidated(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        self.total = 0
        super(payment_voucher_report_consolidated, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'get_month':self._get_month,
            'amount_word': self._amount_word,
            'total':self._total,
            'get_bank':self._get_bank,
        })
    def _get_bank(self):
        return self.bank_name
        
    def set_context(self, objects, data, ids, report_type=None):
        period_obj = self.pool.get('account.period')
        period_id = period_obj.search(self.cr,self.uid, [('name', '=', data['form']['period_id'][1] )])
        self.bank_name = data['form']['bank_id'][1]
        for period in period_obj.browse(self.cr, self.uid, period_id):
            self.date_from = period.date_start
            self.date_to = period.date_stop
        return super(payment_voucher_report_consolidated, self).set_context(objects, data, ids, report_type=report_type)
    def _get_payslip_lines(self, obj, column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        Gross = Entertainment = Over_Payment = Housing = Leave_Grant = Personal_Assistant = Basic = NHIS = Net = NHF = Newspaper_Allowance = Utilities = Personal_Advance = Furniture = Accomodation = CTLS = FGHB = Pension = Salary_Advance = Motor = Under = Domestic_Staff = Meal = Other_Deduction = Tax = Motor_Vehicle_Advance = Transport = RENT = Arrear_Allowance = Peculiar = Acting_Allowance = Overtime = Mv_Adv_Including_Interest = 0.0
        self.bank = obj.bank_id.id
        
        self.cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (self.bank,))
        
        bank_ids = [x[0] for x in self.cr.fetchall()]
        line_name = []
        for bank_id in bank_ids:
            self.cr.execute("select hps.id from hr_payslip_line hp "\
                    "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                    "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                    "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                    "AND he.bank_name = %s", (self.date_from,self.date_to,bank_id,))
            temp = self.cr.fetchone()
            if temp:
                line_name.append(temp[0])
        
        computation_lines = {}
        for line in payslip_line.browse(self.cr, self.uid, line_name):
            for l in line.line_ids:
                computation_lines[l.name]= l.amount
                if l.name == 'Gross':
                    Gross += l.amount
                    computation_lines[l.name]= Gross
                if l.name == 'Entertainment':
                    Entertainment += l.amount
                    computation_lines[l.name] = Entertainment
                if l.name == 'Motor Maintainance and Fueling':
                    Motor += l.amount
                    computation_lines[l.name] = Motor
                if l.name == 'Under Payment':
                    Under += l.amount
                    computation_lines[l.name] = Under 
                if l.name == 'Peculiar Allowances':
                    Peculiar += l.amount
                    computation_lines[l.name] = Peculiar
                if l.name == 'Over Payment':
                    Over_Payment += l.amount
                    computation_lines[l.name] = Over_Payment
                if l.name == 'Housing':
                    Housing += l.amount
                    computation_lines[l.name] = Housing
                if l.name == 'Leave Grant':
                    Leave_Grant += l.amount
                    computation_lines[l.name] = Leave_Grant
                if l.name == 'Personal Assistant':
                    Personal_Assistant += l.amount
                    computation_lines[l.name] = Personal_Assistant
                if l.name == 'Consolidated Allowance':
                    Basic += l.amount
                    computation_lines[l.name] = Basic
                if l.name == 'NHIS':
                    NHIS += l.amount
                    computation_lines[l.name] = NHIS
                if l.name == 'Net':
                    Net += l.amount
                    computation_lines[l.name] = Net
                if l.name == 'NHF':
                    NHF += l.amount
                    computation_lines[l.name] = NHF
                if l.name == 'Newspaper':
                    Newspaper_Allowance += l.amount
                    computation_lines[l.name] = Newspaper_Allowance
                if l.name == 'Utilities':
                    Utilities += l.amount
                    computation_lines[l.name] = Utilities
                if l.name == 'Personal Advance':
                    Personal_Advance += l.amount
                    computation_lines[l.name] = Personal_Advance
                if l.name == 'Furniture':
                    Furniture += l.amount
                    computation_lines[l.name] = Furniture
                if l.name == 'Accomodation':
                    Accomodation += l.amount
                    computation_lines[l.name] = Accomodation
                if l.name == 'CTLS':
                    CTLS += l.amount
                    computation_lines[l.name] = CTLS
                if l.name == 'FGHB':
                    FGHB += l.amount
                    computation_lines[l.name] = FGHB
                if l.name == 'Pension':
                    Pension += l.amount
                    computation_lines[l.name] = Pension
                if l.name == 'Salary Advance':
                    Salary_Advance += l.amount
                    computation_lines[l.name] = Salary_Advance
                if l.name == 'Domestic Staff':
                    Domestic_Staff += l.amount
                    computation_lines[l.name] = Domestic_Staff
                if l.name == 'Meal':
                    Meal += l.amount
                    computation_lines[l.name] = Meal
                if l.name == 'Other Deduction':
                    Other_Deduction += l.amount
                    computation_lines[l.name] = Other_Deduction
                if l.name == 'Tax':
                    Tax += l.amount
                    computation_lines[l.name] = Tax
                if l.name == 'Motor Vehicle Advance':
                    Motor_Vehicle_Advance += l.amount
                    computation_lines[l.name] = Motor_Vehicle_Advance
                if l.name == 'Transport':
                    Transport += l.amount
                    computation_lines[l.name] = Transport
                if l.name == 'Rent':
                    RENT += l.amount
                    computation_lines[l.name] = RENT
                if l.name == 'Arrears':
                    Acting_Allowance += l.amount
                    computation_lines[l.name] = Acting_Allowance
                if l.name == 'Overtime':
                    Overtime += l.amount
                    computation_lines[l.name] = Overtime
                if l.name == 'Mv Adv Including Interest':
                    Mv_Adv_Including_Interest += l.amount
                    computation_lines[l.name] = Mv_Adv_Including_Interest
                if l.name == 'Arrear Allowance':
                    Arrear_Allowance += l.amount
                    computation_lines[l.name] = Arrear_Allowance
                    
        if computation_lines:
            grosss_amount = computation_lines['Consolidated Allowance'] + computation_lines['Arrears'] + computation_lines['Overtime']

            deducation_amount = computation_lines['Tax'] + computation_lines['NHF'] + computation_lines['Other Deduction'] + computation_lines['Pension']+ computation_lines['CTLS'] + computation_lines['NHIS'] + computation_lines['Mv Adv Including Interest'] +computation_lines['Personal Advance']+ computation_lines['Nigerian Region'] + computation_lines['FGHB'] + computation_lines['Over Payment'] + computation_lines['Salary Advance'] 
            
            deduct_voucher = deducation_amount
            
            taxble_1= computation_lines['Meal'] + computation_lines['Housing'] + computation_lines['Transport']+ computation_lines['Furniture'] + computation_lines['Arrears'] + computation_lines['Peculiar Allowances'] + computation_lines['Arrear Allowance'] + computation_lines['Newspaper'] + computation_lines['Motor Maintainance and Fueling']
            
            taxble_2= computation_lines['Entertainment'] + computation_lines['Utilities'] + computation_lines['Domestic Staff'] +computation_lines['Leave Grant'] + computation_lines['Under Payment'] + computation_lines['Accomodation'] + computation_lines['Personal Assistant']
    
            #taxble = taxble_1 + taxble_2
            
            taxble = computation_lines['Peculiar Allowances'] + computation_lines['Arrear Allowance']
            
            net_pay =  grosss_amount - deducation_amount
            
            self.total = taxble + net_pay
            result.append({
                'basic': computation_lines['Consolidated Allowance'], 
                'acting_allow': computation_lines['Arrears'],
                'overtime': computation_lines['Overtime'],
                'gross_amount': grosss_amount,
    
                'tax': computation_lines['Tax'],
                'nhf': computation_lines['NHF'],
                'other_ded': computation_lines['Other Deduction'],
                'pension': computation_lines['Pension'],
                'nhis': computation_lines['NHIS'],
                'ctls': computation_lines['CTLS'],
                'mv_adv_interest': computation_lines['Mv Adv Including Interest'],
                'personl_adv': computation_lines['Personal Advance'],
                'nigerin_reg': computation_lines['Nigerian Region'],
                'fghb': computation_lines['FGHB'],
                'over_payment': computation_lines['Over Payment'],
                'salary_advance': computation_lines['Salary Advance'],
                'deducation_amt': deducation_amount,
                'net_pay': net_pay,
                'meal': computation_lines['Meal'],
                'rent': computation_lines['Housing'],
                'transport':computation_lines['Transport'],  
                'furniture': computation_lines['Furniture'],
                'entertainment': computation_lines['Entertainment'],
                'utilities': computation_lines['Utilities'],
                'domestic_servent': computation_lines['Domestic Staff'],
                'leave_grant': computation_lines['Leave Grant'],
                'arrears': computation_lines['Arrear Allowance'],
                'under_payment': computation_lines['Under Payment'],
                'accomodation': computation_lines['Accomodation'],
                'personal_alw': computation_lines['Personal Assistant'],
                'motor_allw': computation_lines['Motor Maintainance and Fueling'],
                'newspaper': computation_lines['Newspaper'],
                'peculiar': computation_lines['Peculiar Allowances'],
                
                'taxable': taxble, 
                'net_total': taxble + net_pay,
                'motor_vehicle': computation_lines['Motor Vehicle Advance'],
                'deduct_voucher': deduct_voucher,
                #'name' :  computation_lines['employee'],   
                 })
        return result
        
    def _get_month(self, obj):
        month = int(obj.period_id.date_start.split('-')[1])
        return calendar.month_name[month]
    def _total(self):
        return self.total
    def _amount_word(self):
        amount = amount_to_text(self.total)
        word = str(amount) + ' Only'
        return word
report_sxw.report_sxw('report.payroll.summary.report.consolidated', 'hr.payslip', 'addons/payment_voucher_emoluments/report/payment_voucher_report_consolidated.mako', parser=payment_voucher_report_consolidated, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
