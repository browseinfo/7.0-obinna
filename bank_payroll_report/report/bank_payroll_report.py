#!/usr/bin/env python
#-*- coding:utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import operator
import itertools
from datetime import datetime
from dateutil import relativedelta
from tools.translate import _
from report import report_sxw
import netsvc
from osv import fields, osv


class bank_payroll_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bank_payroll_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines': self._get_payslip_lines,
            'get_total': self._get_total,
            'get_name' : self._get_name,
            'multikeysort' : self.multikeysort,
            'call_date': self._call_date,
            'call_date_from': self._call_date_from,
            'call_date_to': self._call_date_to,
            
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
        return super(bank_payroll_report, self).set_context(objects, data, ids, report_type=report_type)

    def _get_name(self, obj,):
        self.bank = obj.bank_id.id
        self.cr.execute("select name from res_bank where id = %s", (self.bank,))
        name = self.cr.fetchone()
        return name[0]
        
    def _call_date(self):
       return time.strftime('%d-%m-%Y')
       
    def _get_total(self, obj,):

        result = []
        basic = acting_allow = overtime = gross_amount = tax = nhf = other_ded = pension =nhis =ctls =underpayment =mv_adv_interest = personl_adv = nigerin_reg = fghb = over_payment = salary_advance = deducation_amt =net_pay = meal = rent = transport=  furniture =  entertainment = utilities=domestic_servent=leave_grant= peculiar=arrear_basic= underpayment = taxable = net_total = total_ae = motor_allw = accomodation = newspaper = personal_alw=  0.0
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
            peculiar+= line['peculiar']
            underpayment += line['underpayment']
            arrear_basic+= line['arrear_basic']
            accomodation+= line['accomodation']
            personal_alw+= line['personal_alw']
            motor_allw+= line['motor_allw']
            newspaper+= line['newspaper']
            
            #underpayment += line['underpayment']
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
                'underpayment': underpayment,
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
                'peculiar' : peculiar,
                'arrear_basic':  arrear_basic,
                'underpayment' : underpayment,
                'accomodation': accomodation,
                'personal_alw': personal_alw,
                'motor_allw': motor_allw,
                'newspaper': newspaper,           
                    
                'taxable': taxable, 
                'net_total': net_total,
                'total_ae': total_ae
                 })
        return result

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
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        self.bank = obj.bank_id.id
        self.cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (self.bank,))
        
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
            for l in line.line_ids:
                    computation_lines[l.name]= l.amount
            res.append({
                            'computation': computation_lines,
                            'employee' : line.employee_id.name,
                            'emp_id' : line.employee_id.id,
                            'rank_id': line.employee_id.rank_id.id
                           })
        for i in res:                           
            grosss_amount = i['computation']['Basic'] + i['computation']['Arrears'] + i['computation']['Overtime']
            print "+ i['computation']['Under Payment']------------",+ i['computation']['Under Payment']
            deducation_amount = i['computation']['Tax'] + i['computation']['NHF'] + i['computation']['Other Deduction'] + i['computation']['Pension']+ i['computation']['NHIS'] + i['computation']['CTLS'] + i['computation']['Mv Adv Including Interest'] +i['computation']['Personal Advance']+ i['computation']['Nigerian Region'] + i['computation']['FGHB'] + i['computation']['Over Payment'] + i['computation']['Salary Advance']
                
            taxble_1= i['computation']['Meal']+ i['computation']['Housing'] + i['computation']['Transport']+ i['computation']['Furniture'] + i['computation']['Arrears'] + i['computation']['Peculiar Allowances'] + i['computation']['Under Payment'] + i['computation']['Arrear Allowance'] + i['computation']['Newspaper'] + i['computation']['Motor Maintainance and Fueling']
            
            taxble_2= i['computation']['Entertainment'] + i['computation']['Utilities'] + i['computation']['Domestic Staff'] + i['computation']['Leave Grant'] + i['computation']['Under Payment'] + i['computation']['Accomodation'] + i['computation']['Personal Assistant']  
            taxble = taxble_1 + taxble_2
            net_pay =  grosss_amount - deducation_amount
            
            result.append({
            'basic': i['computation']['Basic'], 
            'acting_allow': i['computation']['Arrears'],
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
            'peculiar': i['computation']['Peculiar Allowances'],
            'underpayment': i['computation']['Under Payment'],
            'arrear_basic' : i['computation']['Arrear Allowance'],
            'underpayment': i['computation']['Under Payment'],
            'accomodation': i['computation']['Accomodation'],
            'personal_alw': i['computation']['Personal Assistant'],
            'motor_allw': i['computation']['Motor Maintainance and Fueling'],
            'newspaper': i['computation']['Newspaper'],

            'taxable': taxble, 
            'net_total': taxble + net_pay,
            'name' :  i['employee'],   
            'rank_id': i['rank_id'],
            'total_ae': i['computation']['Total Basic']
            
             })
            print "##############'underpayment': i['computation']['Under Payment'],#############",i['computation']['Under Payment']
        self.lines = result
        
        if obj.type == 'amount':
            new_result = self.multikeysort(self.lines, ['-net_total', 'name'])
            return new_result
        else: 
            new_result = self.multikeysort(self.lines, ['-rank_id', 'name'])
            return new_result

        

report_sxw.report_sxw('report.bank.payroll.report.all', 'hr.payslip', 'addons/bank_report/report/bank_payroll_report.mako', parser=bank_payroll_report, header=False)
#report_sxw.report_sxw('report.bank.payroll.report.all', 'hr.payslip', 'addons/bank_report/report/bank_payroll_report.rml', parser=bank_payroll_report, header=False)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
