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


class voucher_payment_deduction(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(voucher_payment_deduction, self).__init__(cr, uid, name, context)
        self.amount_total = 0.0
        self.amount_adv_total = 0.0
        self.amount_n_total = 0.0
        self.dict_vo1 = {}
        self.amt_list = []
        self.localcontext.update({
            'time': time,
            'get_head':self.get_head,
            'get_s_head':self.get_s_head,
            'get_payee':self.get_payee,
            'get_classification_code0':self.get_classification_code0,
            'get_classification_code1':self.get_classification_code1,
            'get_classification_code2':self.get_classification_code2,
            'get_classification_code3':self.get_classification_code3,
            'get_classification_code4':self.get_classification_code4,
            'get_classification_code5':self.get_classification_code5,
            'get_classification_code6':self.get_classification_code6,
            'get_classification_code7':self.get_classification_code7,
            'get_classification_code8':self.get_classification_code8,
            'get_classification_code9':self.get_classification_code9,
            'get_classification_code10':self.get_classification_code10,
            'get_classification_code11':self.get_classification_code11,
            'get_classification_code12':self.get_classification_code12,
            'get_classification_code13':self.get_classification_code13,
            'get_vo1_no0':self.get_vo1_no0,
            'get_vo1_no1':self.get_vo1_no1,
            'get_vo1_no2':self.get_vo1_no2,
            'get_vo1_no3':self.get_vo1_no3,
            'get_vo1_no4':self.get_vo1_no4,
            'get_vo1_no5':self.get_vo1_no5,
            'get_vo1_no6':self.get_vo1_no6,
            'get_vo1_no7':self.get_vo1_no7,
            'get_vo1_no8':self.get_vo1_no8,
            'get_vo1_no9':self.get_vo1_no9,
            'get_vo1_no10':self.get_vo1_no10,
            'get_dept_no':self.get_dept_no,
            'get_payslip_lines':self.get_payslip_lines,
            'get_period':self.get_period,
            'get_total': self.get_total,
            'amount_word': self.amount_word,
            'get_deduction':self.get_deduction,
            'get_adv_total' : self.get_adv_total,
            'get_n_total':self.get_n_total,
            'get_address':self.get_address,
            'get_bank_name':self.get_bank_name,
        })
    def get_bank_name(self,data):
        self.cr.execute("select name from res_bank where id = %s", (data,))
        rows = self.cr.fetchall()
        return rows[0][0]    
    
    def get_head(self,data):
        return data['head']
        
    def get_s_head(self,data):
        return data['s_head']

    def get_payee(self,data):
        return data['payee']

    def get_address(self,data):
        return data['address']
    
    def get_classification_code0(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 1:
            return class_code[0]
        else:
            return ' '
    
    def get_classification_code1(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 2:
            return class_code[1]
        else:
            return ' '   
    
    def get_classification_code2(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 3:
            return class_code[2]
        else:
            return ' '
    
    def get_classification_code3(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 4:
            return class_code[3]
        else:
            return ' '
    
    def get_classification_code4(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 5:
            return class_code[4]
        else:
            return ' '
    
    def get_classification_code5(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 6:
            return class_code[5]
        else:
            return ' '
    
    def get_classification_code6(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 7:
            return class_code[6]
        else:
            return ' '
    
    def get_classification_code7(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 8:
            return class_code[7]
        else:
            return ' '
    
    def get_classification_code8(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 9:
            return class_code[8]
        else:
            return ' '
    
    def get_classification_code9(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 10:
            return class_code[9]
        else:
            return ' '
    
    def get_classification_code10(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 11:
            return class_code[10]
        else:
            return ' '
    
    def get_classification_code11(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 12:
            return class_code[11]
        else:
            return ' '
    
    def get_classification_code12(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 13:
            return class_code[12]
        else:
            return ' '
    
    def get_classification_code13(self,data):
        class_code = list(data['classification_code'])
        if len(class_code) >= 14:
            return class_code[13]
        else:
            return ' '
    
    def get_vo1_no0(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 1:
            return vo1[0]
        else:
            return ' '
    
    def get_vo1_no1(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 2:
            return vo1[1]
        else:
            return ' '
    
    def get_vo1_no2(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 3:
            return vo1[2]
        else:
            return ' '
    
    def get_vo1_no3(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 4:
            return vo1[3]
        else:
            return ' '
    
    def get_vo1_no4(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 5:
            return vo1[4]
        else:
            return ' '
    
    def get_vo1_no5(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 6:
            return vo1[5]
        else:
            return ' '
    
    def get_vo1_no6(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 7:
            return vo1[6]
        else:
            return ' '
    
    def get_vo1_no7(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 8:
            return vo1[7]
        else:
            return ' '
    
    def get_vo1_no8(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 9:
            return vo1[8]
        else:
            return ' '
    
    def get_vo1_no9(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 10:
            return vo1[9]
        else:
            return ' '
    
    def get_vo1_no10(self,data):
        vo1 = list(data['vo1'])
        if len(vo1) >= 11:
            return vo1[10]
        else:
            return ' '
    
    def get_dept_no(self,data):
        return data['department_no']
    
    def get_period(self):
        return self.period
    
    def set_context(self, objects, data, ids, report_type=None):
        self.wizard_period = data['form']['period_id'][0]
        self.date_period = self.pool.get('account.period').browse(self.cr, self.uid, self.wizard_period).date_start
        self.date_end = self.pool.get('account.period').browse(self.cr, self.uid, self.wizard_period).date_stop
        formatter_string = "%Y-%m-%d" 
        datetime_object = datetime.strptime(self.date_period, formatter_string)
        date_object = datetime_object.date()
        self.period = date_object.strftime("%B %Y")
        self.deduction = data['form']['deduction'][1]
        self.category = data['form']['deduction'][0]
        return super(voucher_payment_deduction, self).set_context(objects, data, ids, report_type=report_type)
    
    def get_payslip_lines(self, obj,column_flag=0):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        self.amount_total = 0
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
            self.amt_list.append(amount)
            
            result.append({
                           'amount': amount,
                           'employee': i['employee'],
                           })
            self.amount_total += amount
            
        emp = max(result, key=lambda x:x['amount'])
        return emp['employee']

    def get_total(self):
        return self.amount_total

    def get_adv_total(self, obj):
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        self.amount_adv_total = 0
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
            self.amount_adv_total += amount
        return self.amount_adv_total
    
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
    
    def amount_word(self):
        amount = amount_to_text(self.amount_total)
        word = str(amount) + ' Only'
        return word
    
    def get_deduction(self):
        return self.deduction
        
report_sxw.report_sxw('report.voucher.deduction.report', 'voucher.payment.deduction.wizard', 'voucher_payment_deduction/report/voucher_payment_deduction.rml', parser=voucher_payment_deduction, header=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
