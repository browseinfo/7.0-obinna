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
import xlwt
from xlsxwriter.workbook import Workbook
from tools.translate import _
from cStringIO import StringIO
import base64
import netsvc

from osv import fields, osv

class payment_voucher_wizard(osv.osv_memory):
    _name ='payment.voucher.wizard'

    _columns = {
         'period_id': fields.many2one('account.period', 'Period',  required=True),
         'bank_id': fields.many2one('res.bank', 'Bank Name', required=True),
    }

    def print_report_basic(self, cr, uid, ids, context=None):
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
            'report_name': 'payroll.summary.report',
            'datas': datas,
        }
        
    def print_report_consolidated(self, cr, uid, ids, context=None):
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
            'report_name': 'payroll.summary.report.consolidated',
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
        
        Gross = Entertainment = Over_Payment = Housing = Leave_Grant = Personal_Assistant = Basic = NHIS = Net = NHF = Newspaper_Allowance = Utilities = Personal_Advance = Furniture = Accomodation = CTLS = FGHB = Pension = Salary_Advance = Motor = Under = Domestic_Staff = Meal = Other_Deduction = Tax = Motor_Vehicle_Advance = Transport = RENT  = Peculiar = Acting_Allowance = Overtime = Mv_Adv_Including_Interest = 0.0
        
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
            
                
        computation_lines = {}
        for line in payslip_line.browse(cr, uid, line_name):
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
                'arrears': computation_lines['Arrears'],
                'under_payment': computation_lines['Under Payment'],
                'accomodation': computation_lines['Accomodation'],
                'personal_alw': computation_lines['Personal Assistant'],
                'motor_allw': computation_lines['Motor Maintainance and Fueling'],
                'newspaper': computation_lines['Newspaper'],
                'peculiar': computation_lines['Peculiar Allowances'],
                'arrear_allw': computation_lines['Arrear Allowance'],
                
                'taxable': taxble, 
                'net_total': taxble + net_pay,
                'motor_vehicle': computation_lines['Motor Vehicle Advance'],
                'deduct_voucher': deduct_voucher,
                #'name' :  computation_lines['employee'],   
                 })
                 
        #new_result = self.multikeysort(result, ['-net_total'])
        # Create an new Excel file and add a worksheet.
        today = datetime.strptime(obj.period_id.date_start, '%Y-%m-%d')
        today_date = (str(today.day) + '/' + str(today.month) + '/' + str(today.year))
        import base64
        filename = 'bank_payroll_basic_summary_report.xls'
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
        worksheet.write(0,6, 'NIGERIA FEDERAL GOVEREMENT PAYROLL', style)
        worksheet.write(1,1, 'MINISTRY / DEPARTMENT - FEDERAL JUDICIAL SERVICE COMMISSION', style)
        worksheet.write(2,1, 'T.F.2 PRB (1973)', style)
        worksheet.write(3,0, 'Date', style)
        worksheet.write(3,1, today_date, style)
        worksheet.write(4,1, obj.bank_id.name, style)
        
        first_row = worksheet.row(0)
        first_row.set_style(tall_style)
        col = 0
        column_list = ['BASIC SALARY', 'ACTING ALLOWENCE - ARREAR BASIC', 'OVERTIME','GROSS EMOLUMENTS', 'TAX THIS MONTH', 'NHF', 'OTHER DEDUCTION', 'PENSION', 'NHIS', 'C.T.L.S', 'MV ADV INTEREST', 'UGV PESNONAL ADVANCE', 'NIGERIAN REGION', 'FGHB', 'OVER PAYMENT', 'SALARY ADVANCE', 'TOTAL DEDUCTION', 'NET PAY', 'MEAL SUBSIDY', 'RENT SUBSIDY', 'TRANSPORT ALW', 'FURNITURE ALW', 'ENTERMENT ALW', 'Accomodation', 'Personal Assistant', 'Motor Maintainance and Fueling', 'Newspaper', 'UTILITY', 'DOMESTIC SERVENTS ALW', 'ANNUAL LEAVE GRANT', 'Arrear Basic', 'Perculiar Allowance' , 'UNDER PAYMENT', 'TOTAL NON TAXABLE', 'TOTAL NET EMOLUMENTS']
        
        res_list = [ 'basic' , 'acting_allow' , 'overtime' , 'gross_amount' , 'tax' , 'nhf' , 'other_ded' , 'pension' , 'nhis' ,'ctls' , 'mv_adv_interest' , 'personl_adv' , 'nigerin_reg' , 'fghb' , 'over_payment' , 'salary_advance' , 'deducation_amt' , 'net_pay' , 'meal' , 'rent' , 'transport',  'furniture' ,  'entertainment' , 'accomodation', 'personal_alw', 'motor_allw', 'newspaper', 'utilities', 'domestic_servent', 'leave_grant' , 'arrears', 'peculiar',  'under_payment' , 'taxable' , 'net_total']
        
        rec_list = [ 'basic' , 'acting_allow' , 'overtime' , 'gross_amount' , 'tax' , 'nhf' , 'other_ded' , 'pension' , 'nhis' ,'ctls' , 'mv_adv_interest' , 'personl_adv' , 'nigerin_reg' , 'fghb' , 'over_payment' , 'salary_advance' , 'deducation_amt' , 'net_pay' , 'meal' , 'rent' , 'transport',  'furniture' ,  'entertainment' , 'accomodation', 'personal_alw', 'motor_allw', 'newspaper', 'utilities', 'domestic_servent', 'leave_grant' , 'arrears', 'peculiar', 'under_payment' , 'taxable' , 'net_total']
        
        basic = acting_allow = overtime = gross_amount = tax = nhf = other_ded = pension =nhis =ctls =mv_adv_interest = personl_adv = nigerin_reg = fghb = over_payment = salary_advance = deducation_amt =net_pay = meal = rent = transport=  furniture =  entertainment = personal_alw =accomodation= motor_allw = newspaper = utilities=domestic_servent=leave_grant=arrears=peculiar=arrear_allw=under_payment = taxable = net_total = 0.0

        for i in column_list:
            worksheet.write(6,col, i, style)
            col +=1

        res_final= []
        for line in result:
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
            accomodation+= line['accomodation']
            personal_alw+= line['personal_alw']
            motor_allw+= line['motor_allw']
            newspaper+= line['newspaper']
            utilities+= line['utilities'] 
            domestic_servent+= line['domestic_servent']
            leave_grant+= line['leave_grant']
            arrears+= line['arrears'] 
            peculiar+= line['peculiar'] 
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
                'accomodation': accomodation,
                'personal_alw': personal_alw,
                'motor_allw': motor_allw,
                'newspaper': newspaper,
                'utilities': utilities,
                'domestic_servent': domestic_servent,
                'leave_grant': leave_grant,
                'arrears': arrears,
                'peculiar' : peculiar,
                'under_payment' : under_payment,
    
                'taxable': taxable, 
                'net_total': net_total,
                 })
            
        r = 7
        '''for i in res_final:
            cl = 0
            for j in i['vals']:
                worksheet.write(r,cl, j,)
                cl +=1
            r +=1'''

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
        export_id = self.pool.get('bank.payroll.excel.basic').create(cr, uid, {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename}, context=context)
        fp.close()
        return {
            'view_mode': 'form',
            'res_id': export_id,
            'res_model': 'bank.payroll.excel.basic',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }
        
        return True

payment_voucher_wizard()

class bank_payroll_excel_basic(osv.osv_memory):

    _name= "bank.payroll.excel.basic"
    _columns= {
               'excel_file': fields.binary('payroll Bank Excel Report'),
               'file_name': fields.char('Excel File', size=64),
               }

bank_payroll_excel_basic()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
