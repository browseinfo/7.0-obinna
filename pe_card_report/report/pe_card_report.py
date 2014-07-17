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
from dateutil import parser
from dateutil import relativedelta
from tools.translate import _
from report import report_sxw
import netsvc
from osv import fields, osv


class pe_card_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(pe_card_report, self).__init__(cr, uid, name, context)
        self.lines = []
        
        self.count = self.basic_total = self.acting_allow_total = self.overtime_total = self.gross_amount_total = self.tax_total = self.nhf_total = self.other_ded_total = self.pension_total = self.nhis_total = self.ctls_total = self.mv_adv_interest_total = self.personl_adv_total = self.nigerin_reg_total = self.fghb_total = self.over_payment_total = self.salary_advance_total = self.deducation_amt_total = self.net_pay_total = self.meal_total = self.rent_total = self.transport_total = self.furniture_total = self.entertainment_total = self.utilities_total = self.domestic_servent_total = self.leave_grant_total = self.arrears_total = self.peculiar_total = self.under_payment_total = self.taxable_total = self.net_total_total = self.total_ae_total = 0.0
        
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'get_total': self._get_total,
            'get_name' : self._get_name,
            'get_dob' : self._get_dob,
            'get_gender' : self._get_gender,
            'get_child' : self._get_child,
            'get_emp_name' : self._get_emp_name,
            'get_rank_name' : self._get_rank_name,
            'get_branch_name' : self._get_branch_name,
            'multikeysort' : self.multikeysort,
            'call_date': self._call_date,
            'call_date_from': self._call_date_from,
            'call_date_to': self._call_date_to,
            'get_seq': self._get_seq,
            'get_basic_total': self._get_basic_total,
            'get_acting_allow_total': self._get_acting_allow_total, 
            'get_overtime_total': self._get_overtime_total,
            'get_gross_amount_total': self._get_gross_amount_total,
            'get_tax_total': self._get_tax_total,
            'get_nhf_total': self._get_nhf_total,
            'get_pension_total': self._get_pension_total,
            'get_ctls_total': self._get_ctls_total,
            'get_mv_adv_interest_total': self._get_mv_adv_interest_total,
            'get_personl_adv_total': self._get_personl_adv_total,
            'get_salary_advance_total': self._get_salary_advance_total,
            'get_deducation_amt_total': self._get_deducation_amt_total,
            'get_net_pay_total': self._get_net_pay_total,
            'get_meal_total': self._get_meal_total,
            'get_rent_total': self._get_rent_total,
            'get_transport_total': self._get_transport_total,
            'get_entertainment_total': self._get_entertainment_total,
            'get_utilities_total': self._get_utilities_total,
            'get_leave_grant_total': self._get_leave_grant_total,
            'get_arrears_total': self._get_arrears_total,
            'get_taxable_total': self._get_taxable_total,
            'get_net_total_total': self._get_net_total_total,
        })
        
    def _call_date_from(self, obj):
        date = datetime.strptime(self.date_from, '%Y-%m-%d')
        return (str(date.day) + '-' + str(date.month) + '-' + str(date.year))
        
    def _call_date_to(self, obj):
        date = datetime.strptime(self.date_to, '%Y-%m-%d')
        return (str(date.day) + '-' + str(date.month) + '-' + str(date.year))
        
    def _get_seq(self):
        self.count += 1
        return self.count

    def set_context(self, objects, data, ids, report_type=None):
        hr_obj = self.pool.get('hr.employee')
        emp_ids = hr_obj.search(self.cr,self.uid, [('name', '=', data['form']['employee_id'][1] )])
        emp = hr_obj.browse(self.cr, self.uid, emp_ids)[0]
        self.emp_id = emp.id
        self.emp_name = emp.name
        return super(pe_card_report, self).set_context(objects, data, ids, report_type=report_type)

    def _get_name(self, form):
        self.emp_id = form.get('employee_id')[0]
        self.cr.execute("select bank_name from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        self.cr.execute("select bank_name from res_partner_bank where id = %s ", (name))
        bank_name = self.cr.fetchone()
        if bank_name:
            return bank_name[0]
        
    def _get_emp_name(self, form):
        self.cr.execute("select name_related from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        if name:
            return name[0]
        
    def _get_dob(self, form):
        self.cr.execute("select birthday from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        if name:
            return name[0]
        
    def _get_child(self, form):
        self.cr.execute("select children from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        if name:
            return name[0]
        
    def _get_gender(self, form):
        self.cr.execute("select gender from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        if name:
            return name[0]
        
    def _get_rank_name(self, form):
        self.cr.execute("select rank_id from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        
        self.cr.execute("select grade_id from grade_step where id = %s ", (name))
        grade = self.cr.fetchone()
        self.cr.execute("select name from grade where id = %s ", (grade))
        grade_name = self.cr.fetchone()
        
        self.cr.execute("select step_id from grade_step where id = %s ", (name))
        step = self.cr.fetchone()
        self.cr.execute("select name from step where id = %s ", (step))
        step_name = self.cr.fetchone()
        return grade_name[0] + ' - ' + step_name[0] 
        
    def _get_branch_name(self, form):
        self.cr.execute("select bank_name from hr_employee where id = %s", (self.emp_id,))
        name = self.cr.fetchone()
        self.cr.execute("select branch_code from res_partner_bank where id = %s ", (name))
        branch_name = self.cr.fetchone()
        if branch_name:
            return branch_name[0]
        
    def _call_date(self):
       return time.strftime('%d-%m-%Y')
       
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

    def _get_payslip_lines(self, obj, column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        payslip_lines = []
        res = []
        result = []
        jan_from = time.strftime('%Y-01-01')
        jan_to = time.strftime('%Y-01-31')
        feb_from = time.strftime('%Y-02-01')
        feb_to = time.strftime('%Y-02-28')
        
        self.cr.execute("select DISTINCT hps.id from hr_payslip_line hp "\
                "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                "LEFT JOIN hr_employee he on (hps.employee_id = he.id) "\
                "WHERE (he.id = %s) "\
                , (self.emp_id,))
                
        line_name = [i[0] for i in self.cr.fetchall()]
        for line in payslip_line.browse(self.cr, self.uid, line_name):
            computation_lines = {}
            for l in line.line_ids:
                computation_lines[l.name]= l.amount
            res.append({
                'computation': computation_lines,
                'employee' : line.employee_id.name,
                'emp_id' : line.employee_id.id,
                'date_month': line.date_from
            })
        for i in res:
            grosss_amount = i['computation']['Basic'] + i['computation']['Acting Allowance'] + i['computation']['Overtime']
            
            deducation_amount = i['computation']['Tax'] + i['computation']['NHF'] + i['computation']['Other Deduction'] + i['computation']['Pension']+ i['computation']['NHIS'] + i['computation']['CTLS'] + i['computation']['Mv Adv Including Interest'] +i['computation']['Personal Advance']+ i['computation']['Nigerian Region'] + i['computation']['FGHB'] + i['computation']['Over Payment'] + i['computation']['Salary Advance']
            
            taxble_1= i['computation']['Meal']+ i['computation']['Housing'] + i['computation']['Transport']+ i['computation']['Furniture'] + i['computation']['Arrears'] + i['computation']['Peculiar Allowances'] 
            
            taxble_2= i['computation']['Entertainment'] + i['computation']['Utilities'] + i['computation']['Domestic Staff'] + i['computation']['Leave Grant'] + i['computation']['Under Payment']

            taxble = taxble_1 + taxble_2
            net_pay =  grosss_amount - deducation_amount
            
            date = datetime.strptime(i['date_month'], '%Y-%m-%d')
            month = {'1':'JANUARY',
                 '2':'FEBRUARY',
                 '3':'MARCH',
                 '4':'APRIL',
                 '5':'MAY',
                 '6':'JUNE',
                 '7':'JULY',
                 '8':'AUGUST',
                 '09':'SEPTEMBER',
                 '10':'OCTOBER',
                 '11':'NOVEMBER',
                 '12':'DECEMBER',
                }
            for key, value in month.iteritems():
                if int(key) == date.month:
                    result.append({
                    'basic': i['computation']['Basic'], 
                    'acting_allow': i['computation']['Acting Allowance'],
                    'overtime': i['computation']['Overtime'],
                    'gross_amount': grosss_amount,

                    'tax': i['computation']['Tax'],
                    'nhf': i['computation']['NHF'],
                    'other_ded': i['computation']['Other Deduction'],
                    'pension': i['computation']['Pension'],
                    'nhis': i['computation']['NHIS'],
                    'ctls': i['computation']['CTLS'],
                    'mv_adv_interest': i['computation']['Mv Adv Including Interest'],
                    'personl_adv': i['computation']['Personal Advance'],
                    'nigerin_reg': i['computation']['Nigerian Region'],
                    'fghb': i['computation']['FGHB'],
                    'over_payment': i['computation']['Over Payment'],
                    'salary_advance': i['computation']['Salary Advance'],
                    'deducation_amt': deducation_amount,

                    'net_pay': net_pay,

                    'meal': i['computation']['Meal'],
                    'rent': i['computation']['Housing'],
                    'transport':i['computation']['Transport'],  
                    'furniture': i['computation']['Furniture'],
                    'entertainment': i['computation']['Entertainment'],
                    'utilities': i['computation']['Utilities'],
                    'domestic_servent': i['computation']['Domestic Staff'],
                    'leave_grant': i['computation']['Leave Grant'],
                    'arrears': i['computation']['Arrears'],
                    'peculiar': i['computation']['Peculiar Allowances'],
                    'under_payment': i['computation']['Under Payment'],

                    'taxable': taxble, 
                    'net_total': taxble + net_pay,
                    'name' :  i['employee'],   
                    'total_ae': i['computation']['Total Basic'],
                    'month': value,
                    'int_month': int(key)
                     })

        self.lines = result
        new_result = self.multikeysort(self.lines, ['int_month', 'name'])
        self._get_total(self.lines)
        return new_result

    def _get_total(self, obj,):

        result = []
        basic = acting_allow = overtime = gross_amount = tax = nhf = other_ded = pension =nhis =ctls =mv_adv_interest = personl_adv = nigerin_reg = fghb = over_payment = salary_advance = deducation_amt =net_pay = meal = rent = transport=  furniture =  entertainment = utilities=domestic_servent=leave_grant=arrears = peculiar= under_payment = taxable = net_total = total_ae = 0.0
        
        for line in self.lines:
            basic +=  line['basic']
            acting_allow += line['acting_allow']
            overtime += line['overtime']
            gross_amount += line['gross_amount'] 
            tax += line['tax']            
            nhf += line['nhf'] 
            other_ded += line['other_ded'] 
            pension += line['pension']
            nhis += line['nhis']
            ctls += line['ctls'] 
            mv_adv_interest += line['mv_adv_interest']        
            personl_adv += line['personl_adv'] 
            nigerin_reg += line['nigerin_reg'] 
            fghb+= line['fghb'] 
            over_payment += line['over_payment'] 
            salary_advance += line['salary_advance'] 
            deducation_amt += line['deducation_amt']
            net_pay += line['net_pay'] 
            meal += line['meal'] 
            rent += line['rent'] 
            transport+= line['transport']  
            furniture += line['furniture'] 
            entertainment += line['entertainment'] 
            utilities+= line['utilities'] 
            domestic_servent+= line['domestic_servent']
            leave_grant+= line['leave_grant']
            arrears+= line['arrears']
            peculiar+= line['peculiar']
            
            under_payment += line['under_payment']
            taxable += line['taxable']
            net_total += line['net_total']
            total_ae += line['total_ae']
        
        result.append({
                'basic': basic, 
                'acting_allow': acting_allow,
                'overtime': overtime,
                'gross_amount': gross_amount,
    
                'tax': tax,
                'nhf': nhf,
                'other_ded': other_ded,
                'pension': pension,
                'nhis': nhis,
                'ctls': ctls,
                'mv_adv_interest': mv_adv_interest,
                'personl_adv': personl_adv,
                'nigerin_reg': nigerin_reg,
                'fghb': fghb,
                'over_payment': over_payment,
                'salary_advance': salary_advance,
                'deducation_amt': deducation_amt,
    
                'net_pay': net_pay,
    
                'meal': meal,
                'rent': rent,
                'transport':transport,  
                'furniture': furniture,
                'entertainment': entertainment,
                'utilities': utilities,
                'domestic_servent': domestic_servent,
                'leave_grant': leave_grant,
                'arrears': arrears,
                'peculiar' : peculiar,
                'under_payment' : under_payment,
    
                'taxable': taxable, 
                'net_total': net_total,
                'total_ae': total_ae
                 })
           
        self.basic_total = result[0]['basic']
        self.acting_allow_total = result[0]['acting_allow']
        self.overtime_total = result[0]['overtime']
        self.gross_amount_total = result[0]['gross_amount']
        self.tax_total = result[0]['tax']
        self.nhf_total = result[0]['nhf']
        self.pension_total = result[0]['pension']
        self.ctls_total = result[0]['ctls']
        self.mv_adv_interest_total = result[0]['mv_adv_interest']
        self.personl_adv_total = result[0]['personl_adv']
        self.salary_advance_total = result[0]['salary_advance']
        self.deducation_amt_total = result[0]['deducation_amt']
        self.net_pay_total = result[0]['net_pay']
        self.meal_total = result[0]['meal']
        self.rent_total = result[0]['rent']
        self.transport_total = result[0]['transport']
        self.entertainment_total = result[0]['entertainment']
        self.utilities_total = result[0]['utilities']
        self.leave_grant_total = result[0]['leave_grant']
        self.arrears_total = result[0]['arrears']
        self.taxable_total = result[0]['taxable']
        self.net_total_total = result[0]['net_total']
         
        return result
        
    def _get_basic_total(self):
        return self.basic_total
        
    def _get_tax_total(self):
        return self.tax_total
        
    def _get_net_total_total(self):
        return self.net_total_total
        
    def _get_taxable_total(self):
        return self.taxable_total
    
    def _get_arrears_total(self):
        return self.arrears_total
        
    def _get_leave_grant_total(self):
        return self.leave_grant_total
        
    def _get_rent_total(self):
        return self.rent_total
        
    def _get_utilities_total(self):
        return self.utilities_total
        
    def _get_entertainment_total(self):
        return self.entertainment_total
        
    def _get_meal_total(self):
        return self.meal_total
        
    def _get_transport_total(self):
        return self.transport_total
        
    def _get_net_pay_total(self):
        return self.net_pay_total
        
    def _get_deducation_amt_total(self):
        return self.deducation_amt_total
        
    def _get_salary_advance_total(self):
        return self.salary_advance_total
        
    def _get_personl_adv_total(self):
        return self.personl_adv_total
        
    def _get_ctls_total(self):
        return self.ctls_total
        
    def _get_mv_adv_interest_total(self):
        return self.mv_adv_interest_total
        
    def _get_pension_total(self):
        return self.pension_total
        
    def _get_nhf_total(self):
        return self.nhf_total
        
    def _get_acting_allow_total(self):
        return self.acting_allow_total
        
    def _get_overtime_total(self):
        return self.overtime_total
        
    def _get_gross_amount_total(self):
        return self.gross_amount_total

report_sxw.report_sxw('report.pe.card.report.all.rml', 'hr.payslip', 'addons/pe_card_report/report/pe_card_report.rml', parser=pe_card_report, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
