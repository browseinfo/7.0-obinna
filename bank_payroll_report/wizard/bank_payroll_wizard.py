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
import xlwt
from xlsxwriter.workbook import Workbook
from tools.translate import _
from cStringIO import StringIO
import base64
import netsvc

from osv import fields, osv

class bank_payroll_wizard(osv.osv_memory):
    _name ='bank.payroll.wizard'

    _columns = {
         'period_id': fields.many2one('account.period', 'Period',  required=True),
         'bank_id': fields.many2one('res.bank', 'Bank Name', required=True),
         'type': fields.selection([('amount', 'Net Amount'),
                                ('grade_step', 'Grade and Step')], 'Sort By', required=True) 
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
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'bank.payroll.report.all',
            'datas': datas,
        }
        

    def print_report_consildatd(self, cr, uid, ids, context=None):
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
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'bank.payroll.consolidate.report.all',
            'datas': datas,
        }


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

    def print_consildatd_excel(self, cr, uid, ids, context=None):
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
        period_obj = self.pool.get('account.period')
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        total = []
        obj = self.browse(cr, uid, ids, context=context)[0]
        bank = obj.bank_id.id
        
        cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (bank,))
        bank_ids = [x[0] for x in cr.fetchall()]
        line_name = []
        for bank_id in bank_ids:
            cr.execute("select hps.id from hr_payslip_line hp "\
                    "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                    "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                    "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                    "AND he.bank_name = %s", (obj.period_id.date_start, obj.period_id.date_stop, bank_id,))
            temp = cr.fetchone()
            if temp:
                line_name.append(temp[0])
        if not line_name:
            raise osv.except_osv(_('Warring!'), _('There is no payroll bank details'))
        
        for line in payslip_line.browse(cr, uid, line_name):
            computation_lines = {}
            for l in line.line_ids:
                    computation_lines[l.name]= l.amount
            res.append({
                            'computation': computation_lines,
                            'employee' : line.employee_id.name,
                            'emp_id' : line.employee_id.id,
                           })
        for i in res:
            grosss_amount = i['computation']['Consolidated Allowance'] + i['computation']['Arrears'] + i['computation']['Overtime']
            deducation_amount = i['computation']['Tax'] + i['computation']['NHF'] + i['computation']['Other Deduction'] + i['computation']['Pension']+ i['computation']['NHIS'] + i['computation']['CTLS'] + i['computation']['Mv Adv Including Interest'] +i['computation']['Personal Advance']+ i['computation']['FGHB'] + i['computation']['Over Payment'] + i['computation']['Salary Advance']
            
            taxble = i['computation']['Peculiar Allowances'] + i['computation']['Under Payment'] + i['computation']['Arrear Allowance']
            net_pay =  grosss_amount - deducation_amount
            
            result.append({
            'basic': i['computation']['Consolidated Allowance'], 
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
            'fghb': i['computation']['FGHB'],
            'over_payment': i['computation']['Over Payment'],
            'salary_advance': i['computation']['Salary Advance'],
            'deducation_amt': deducation_amount,

            'net_pay': net_pay,
            'meal': 0.00,
            'rent': 0.00,
            'transport':0.00,  
            'furniture': 0.00,
            'entertainment': 0.00,
            'accomodation': 0.00,
            'personal_alw': 0.00,
            'motor_allw': 0.00,
            'newspaper': 0.00,
            'utilities': 0.00,
            'domestic_servent': 0.00,
            'leave_grant': 0.00,

            'peculiar': i['computation']['Peculiar Allowances'],
            'underpayment': i['computation']['Under Payment'],
            'arrear_basic' : i['computation']['Arrear Allowance'],
    
            'taxable': taxble, 
            'net_total': taxble + net_pay,
            'name' :  i['employee'],   
            
             })
        new_result = self.multikeysort(result, ['-net_total', 'name'])
        today = datetime.strptime(obj.period_id.date_start, '%Y-%m-%d')
        today_date = (str(today.day) + '/' + str(today.month) + '/' + str(today.year))
        # Create an new Excel file and add a worksheet.
        import base64
        filename = 'hr_bank_payroll_Consolidated_report.xls'
        workbook = xlwt.Workbook()
        style = xlwt.XFStyle()
        tall_style = xlwt.easyxf('font:height 720;') # 36pt
        # Create a font to use with the style
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.height = 250
        style.font = font
        worksheet = workbook.add_sheet('Sheet 1')
        worksheet.write(0,6, 'NIGERIA FEDERAL GOVERNMENT PAYROLL', style)
        worksheet.write(1,1, 'MINISTRY / DEPARTMENT - FEDERAL JUDICIAL SERVICE COMMISSION', style)
        worksheet.write(1,17, 'SHEET NUMBER', style)
        worksheet.write(2,1, 'T.F.2 PRB (1973)', style)
        worksheet.write(3,0, 'Date', style)
        worksheet.write(3,1, today_date, style)
        worksheet.write(4,1, obj.bank_id.name, style)
        
        first_row = worksheet.row(0)
        first_row.set_style(tall_style)
        col = 0
        column_list = ['Consolidated Allowance', 'ACTINGALW.', 'OVERTIME','GROSS EMOLUMENTS', 'TAX THIS MONTH', 'NHF', 'Other Ded.', 'PENSION', 'NHIS', 'C.T.L.S', 'MV ADV INTEREST', 'UGV PERS. ADV.', 'FGHB', 'OVER PAYMENT', 'SALARY ADV.', 'TOTAL DEDUCTION', 'NET PAY', 'MEAL SUBSIDY', 'RENT SUBSIDY', 'TRANS. ALW', 'FURN. ALW', 'ENT. ALW', 'ACC. ALW', 'PERS. ASS. ALW', 'Motor Alw.', 'Newspaper', 'UTILITY', 'DOM. SERV. ALW', 'ANNUAL LEAVE GRANT', 'Peculiar Allowance', 'Under Payment', 'Arrear Allowance', 'TOTAL NON TAXABLE', 'TOTAL NET EMOLUMENTS', 'NAME', 'SIGN']
        
        res_list = [ 'basic' , 'acting_allow' , 'overtime' , 'gross_amount' , 'tax' , 'nhf' , 'other_ded' , 'pension' , 'nhis' ,'ctls' , 'mv_adv_interest' , 'personl_adv' , 'fghb' , 'over_payment' , 'salary_advance' , 'deducation_amt' , 'net_pay' ,'meal' , 'rent' , 'transport',  'furniture' ,  'entertainment' , 'accomodation', 'personal_alw', 'motor_allw', 'newspaper', 'utilities', 'domestic_servent', 'leave_grant' , 'peculiar', 'underpayment', 'arrear_basic', 'taxable' , 'net_total', 'name']
        
        rec_list = [ 'basic' , 'acting_allow' , 'overtime' , 'gross_amount' , 'tax' , 'nhf' , 'other_ded' , 'pension' , 'nhis' ,'ctls' , 'mv_adv_interest' , 'personl_adv' ,'fghb' , 'over_payment' , 'salary_advance' , 'deducation_amt' , 'net_pay' ,'meal' , 'rent' , 'transport',  'furniture' ,  'entertainment' , 'accomodation', 'personal_alw', 'motor_allw', 'newspaper', 'utilities', 'domestic_servent', 'leave_grant' ,'peculiar','underpayment', 'arrear_basic', 'taxable' , 'net_total']
        basic = acting_allow = overtime = gross_amount = tax = nhf = other_ded = pension =nhis =ctls =mv_adv_interest = personl_adv = fghb = over_payment = salary_advance = deducation_amt =net_pay = meal = rent = transport=  furniture =  entertainment = personal_alw =accomodation= motor_allw = newspaper = utilities=domestic_servent=leave_grant= peculiar=underpayment= arrear_basic=taxable = net_total = 0.0

        for i in column_list:
            worksheet.write(6,col, i, style)
            col +=1

        res_final= []
        for line in new_result:
            mid = {"vals":[]}
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
            fghb+= line['fghb'] 
            over_payment += line['over_payment'] 
            salary_advance += line['salary_advance'] 
            deducation_amt += line['deducation_amt']
            net_pay += line['net_pay'] 
            meal = 0.00
            rent = 0.00
            transport = 0.00
            furniture = 0.00 
            entertainment = 0.00 
            accomodation = 0.00
            personal_alw = 0.00
            motor_allw = 0.00
            newspaper = 0.00
            utilities = 0.00
            domestic_servent = 0.00
            leave_grant = 0.00
            peculiar+= line['peculiar'] 
            underpayment+= line['underpayment']
            arrear_basic+= line['arrear_basic']
            taxable += line['taxable']
            net_total += line['net_total']

            for column in res_list:
                mid['vals'].append(line[column])
            res_final.append(mid)

        total.append({
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
                'accomodation': accomodation,
                'personal_alw': personal_alw,
                'motor_allw': motor_allw,
                'newspaper': newspaper,
                'utilities': utilities,
                'domestic_servent': domestic_servent,
                'leave_grant': leave_grant,
    
                'peculiar' : peculiar,
                'underpayment' : underpayment,
                'arrear_basic':  arrear_basic,
    
                'taxable': taxable, 
                'net_total': net_total,
                 })
            
        r = 7
        for i in res_final:
            cl = 0
            for j in i['vals']:
                worksheet.write(r,cl, j,)
                cl +=1
            r +=1

        tot_final= []
        for i in total:
            tid = {"vals":[]}
            for column in rec_list:
                tid['vals'].append(i[column])
            tot_final.append(tid)


        for i in tot_final:
            cl = 0
            for j in i['vals']:
                worksheet.write(r+1,cl, j, style)
                cl +=1
            worksheet.write(r+1,cl, 'TOTAL', style)


        fp = StringIO()
        workbook.save(fp)
        export_id = self.pool.get('bank.payroll.excel').create(cr, uid, {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename}, context=context)
        fp.close()
        return {
                        'view_mode': 'form',
                        'res_id': export_id,
                        'res_model': 'bank.payroll.excel',
                        'view_type': 'form',
                        'type': 'ir.actions.act_window',
                        'context': context,
                        'target': 'new',
                }
               
        
        return True
     
    def print_excel(self, cr, uid, ids, context=None):
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
        period_obj = self.pool.get('account.period')
        payslip_line = self.pool.get('hr.payslip')
        bank_obj = self.pool.get('res.partner.bank')
        payslip_lines = []
        res = []
        result = []
        total = []
        obj = self.browse(cr, uid, ids, context=context)[0]
        bank = obj.bank_id.id
        
        cr.execute("select id from res_partner_bank where bank in (select id from res_bank where id = %s)", (bank,))
        bank_ids = [x[0] for x in cr.fetchall()]
        line_name = []
        for bank_id in bank_ids:
            cr.execute("select hps.id from hr_payslip_line hp "\
                    "LEFT JOIN hr_payslip hps on (hp.slip_id = hps.id) "\
                    "LEFT JOIN hr_employee he on (hp.employee_id = he.id) "\
                    "WHERE (hps.date_from >= %s) AND (hps.date_to <= %s) "\
                    "AND he.bank_name = %s", (obj.period_id.date_start, obj.period_id.date_stop, bank_id,))
            temp = cr.fetchone()
            if temp:
                line_name.append(temp[0])
        if not line_name:
            raise osv.except_osv(_('Warring!'), _('There is no payroll bank details'))
        
        for line in payslip_line.browse(cr, uid, line_name):
            computation_lines = {}
            for l in line.line_ids:
                    computation_lines[l.name]= l.amount
            res.append({
                            'computation': computation_lines,
                            'employee' : line.employee_id.name,
                            'emp_id' : line.employee_id.id,
                           })
        for i in res:
            grosss_amount = i['computation']['Basic'] + i['computation']['Arrears'] + i['computation']['Overtime']
            deducation_amount = i['computation']['Tax'] + i['computation']['NHF'] + i['computation']['Other Deduction'] + i['computation']['Pension']+ i['computation']['NHIS'] + i['computation']['CTLS'] + i['computation']['Mv Adv Including Interest'] +i['computation']['Personal Advance']+ i['computation']['FGHB'] + i['computation']['Over Payment'] + i['computation']['Salary Advance']
            
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
            'underpayment': i['computation']['Under Payment'],
            'arrear_basic' : i['computation']['Arrear Allowance'],
            'under_payment': i['computation']['Under Payment'],
            'accomodation': i['computation']['Accomodation'],
            'personal_alw': i['computation']['Personal Assistant'],
            'motor_allw': i['computation']['Motor Maintainance and Fueling'],
            'newspaper': i['computation']['Newspaper'],
                
            'taxable': taxble, 
            'net_total': taxble + net_pay,
            'name' :  i['employee'],   
            
             })
        new_result = self.multikeysort(result, ['-net_total', 'name'])
        # Create an new Excel file and add a worksheet.
        today = datetime.strptime(obj.period_id.date_start, '%Y-%m-%d')
        today_date = (str(today.day) + '/' + str(today.month) + '/' + str(today.year))
        import base64
        filename = 'hr_bank_payroll_report.xls'
        workbook = xlwt.Workbook()
        style = xlwt.XFStyle()
        tall_style = xlwt.easyxf('font:height 720;') # 36pt
        # Create a font to use with the style
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.height = 250
        style.font = font
        worksheet = workbook.add_sheet('Sheet 1')
        worksheet.write(0,6, 'NIGERIA FEDERAL GOVERNMENT PAYROLL', style)
        worksheet.write(1,1, 'MINISTRY / DEPARTMENT - FEDERAL JUDICIAL SERVICE COMMISSION', style)
        worksheet.write(1,17, 'SHEET NUMBER', style)
        worksheet.write(2,1, 'T.F.2 PRB (1973)', style)
        worksheet.write(3,0, 'Date', style)
        worksheet.write(3,1, today_date, style)
        worksheet.write(4,1, obj.bank_id.name, style)
        
        first_row = worksheet.row(0)
        first_row.set_style(tall_style)
        col = 0
        column_list = ['BASIC SALARY', 'ACTINGALW.', 'OVERTIME','GROSS EMOLUMENTS', 'TAX THIS MONTH', 'NHF', 'Other Ded.', 'PENSION', 'NHIS', 'C.T.L.S', 'MV ADV INTEREST', 'UGV PERS. ADV.', 'FGHB', 'OVER PAYMENT', 'SALARY ADV.', 'TOTAL DEDUCTION', 'NET PAY', 'MEAL SUBSIDY', 'RENT SUBSIDY', 'TRANS. ALW', 'FURN. ALW', 'ENT. ALW', 'ACC. ALW', 'PERS. ASS. ALW', 'Motor Alw.', 'Newspaper', 'UTILITY', 'DOM. SERV. ALW', 'ANNUAL LEAVE GRANT', 'Peculiar Allowance' , 'Under Payment', 'Arrear Allowance','UNDER PAYMENT', 'TOTAL NON TAXABLE', 'TOTAL NET EMOLUMENTS', 'NAME', 'SIGN']
        res_list = [ 'basic' , 'acting_allow' , 'overtime' , 'gross_amount' , 'tax' , 'nhf' , 'other_ded' , 'pension' , 'nhis' ,'ctls' , 'mv_adv_interest' , 'personl_adv' , 'fghb' , 'over_payment' , 'salary_advance' , 'deducation_amt' , 'net_pay' , 'meal' , 'rent' , 'transport',  'furniture' ,  'entertainment' , 'accomodation', 'personal_alw', 'motor_allw', 'newspaper', 'utilities', 'domestic_servent', 'leave_grant' , 'peculiar', 'underpayment', 'arrear_basic', 'under_payment' , 'taxable' , 'net_total', 'name']
        rec_list = [ 'basic' , 'acting_allow' , 'overtime' , 'gross_amount' , 'tax' , 'nhf' , 'other_ded' , 'pension' , 'nhis' ,'ctls' , 'mv_adv_interest' , 'personl_adv' , 'fghb' , 'over_payment' , 'salary_advance' , 'deducation_amt' , 'net_pay' , 'meal' , 'rent' , 'transport',  'furniture' ,  'entertainment' , 'accomodation', 'personal_alw', 'motor_allw', 'newspaper', 'utilities', 'domestic_servent', 'leave_grant' , 'peculiar', 'underpayment','arrear_basic', 'under_payment' , 'taxable' , 'net_total']
        basic = acting_allow = overtime = gross_amount = tax = nhf = other_ded = pension =nhis =ctls =mv_adv_interest = personl_adv = fghb = over_payment = salary_advance = deducation_amt =net_pay = meal = rent = transport=  furniture =  entertainment = personal_alw =accomodation= motor_allw = newspaper = utilities=domestic_servent=leave_grant=peculiar=underpayment=arrear_basic=under_payment = taxable = net_total = 0.0

        for i in column_list:
            worksheet.write(6,col, i, style)
            col +=1

        res_final= []
        for line in new_result:
            mid = {"vals":[]}
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
            accomodation+= line['accomodation']
            personal_alw+= line['personal_alw']
            motor_allw+= line['motor_allw']
            newspaper+= line['newspaper']
            utilities+= line['utilities'] 
            domestic_servent+= line['domestic_servent']
            leave_grant+= line['leave_grant']
            peculiar+= line['peculiar'] 
            underpayment+= line['underpayment'] 
            arrear_basic+= line['arrear_basic']
            under_payment += line['under_payment']
            taxable += line['taxable']
            net_total += line['net_total']

            for column in res_list:
                mid['vals'].append(line[column])
            res_final.append(mid)

        total.append({
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
                'accomodation': accomodation,
                'personal_alw': personal_alw,
                'motor_allw': motor_allw,
                'newspaper': newspaper,
                'utilities': utilities,
                'domestic_servent': domestic_servent,
                'leave_grant': leave_grant,
                'peculiar' : peculiar,
                'underpayment':underpayment,
                'arrear_basic':  arrear_basic,
                'under_payment' : under_payment,
    
                'taxable': taxable, 
                'net_total': net_total,
                 })
            
        r = 7
        for i in res_final:
            cl = 0
            for j in i['vals']:
                worksheet.write(r,cl, j,)
                cl +=1
            r +=1

        tot_final= []
        for i in total:
            tid = {"vals":[]}
            for column in rec_list:
                tid['vals'].append(i[column])
            tot_final.append(tid)


        for i in tot_final:
            cl = 0
            for j in i['vals']:
                worksheet.write(r+1,cl, j, style)
                cl +=1
            worksheet.write(r+1,cl, 'TOTAL', style)


        fp = StringIO()
        workbook.save(fp)
        export_id = self.pool.get('bank.payroll.excel').create(cr, uid, {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename}, context=context)
        fp.close()
        return {
                        'view_mode': 'form',
                        'res_id': export_id,
                        'res_model': 'bank.payroll.excel',
                        'view_type': 'form',
                        'type': 'ir.actions.act_window',
                        'context': context,
                        'target': 'new',
                }
        
        return True


bank_payroll_wizard()

class bank_payroll_excel(osv.osv_memory):

    _name= "bank.payroll.excel"
    _columns= {
               'excel_file': fields.binary('payroll Bank Excel Report'),
               'file_name': fields.char('Excel File', size=64),
               }

bank_payroll_excel()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
