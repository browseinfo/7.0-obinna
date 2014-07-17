# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################
from datetime import datetime
import time
from collections import defaultdict
from openerp.report import report_sxw

class payslip_march_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(payslip_march_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_payslip_lines':self.get_payslip_lines,
            'get_year_month': self.get_year_month,
            'get_year': self._get_year,
            'get_file_number': self._get_file_number,
            'get_name': self._get_name,
            'get_sex': self._get_sex,
            'get_step': self._get_step,
            'get_grade': self._get_grade,
            'get_bank': self._get_bank,
            'get_acc_no': self._get_acc_no,
            'get_sort_code': self._get_sort_code,
            'call_date_from': self._call_date_from,
            'call_date_to': self._call_date_to,
            'get_total_basic_salary': self._get_total_basic_salary,
            
        })
        
    def _call_date_from(self, obj):
        date = datetime.strptime(obj.date_from, '%Y-%m-%d')
        return (str(date.day) + '.' + str(date.month) + '.' + str(date.year))
        
    def _call_date_to(self, obj):
        date = datetime.strptime(obj.date_to, '%Y-%m-%d')
        return (str(date.day) + '.' + str(date.month) + '.' + str(date.year))
               
    def _get_year(self, obj):
        year = datetime.strptime(obj.date_from, '%Y-%m-%d')
        return year.year
    
    def _get_file_number(self, obj):
        if obj.employee_id.file_number:
            return obj.employee_id.file_number
        else:
            return ' ' 
        
    def _get_name(self, obj):
            return obj.employee_id.name
        
    def _get_sex(self, obj):
        sex = obj.employee_id.gender
        if sex == 'male':
            return 'Male'
        elif sex == 'female':
            return 'Female'
        else:
            return ' ' 
        
    def _get_step(self, obj):
        if obj.employee_id.rank_id.step_id:
            return obj.employee_id.rank_id.step_id.name
        else:
            return ' '
            
    def _get_grade(self, obj):
        if obj.employee_id.rank_id.grade_id:
            return obj.employee_id.rank_id.grade_id.name
        else:
            return ' '
        
    def _get_bank(self, obj):
        bank = obj.employee_id.bank_name.bank_name
        if bank:
            return bank
        else:
            return ' '
        
    def _get_acc_no(self, obj):
        bank = obj.employee_id.bank_name.acc_number
        if bank:
            return bank
        else:
            return ' '
        
    def _get_sort_code(self, obj):
        bank = obj.employee_id.bank_name.sort_code
        if bank:
            return bank
        else:
            return ' '
            
    def _get_total_basic_salary(self, obj):
        wage = self.get_payslip_lines(obj.line_ids)
        return  (wage['total_basic_salary'])
        

    def get_payslip_lines(self, obj):
        payslip_line = self.pool.get('hr.payslip.line')
        res = []
        ids = []
        for id in range(len(obj)):
            if obj[id].appears_on_payslip == True:
                ids.append(obj[id].id)
        if ids:
            res = payslip_line.browse(self.cr, self.uid, ids)
            wages = {}
            for i in res:
                wages[i.name] = i.amount
                
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
            
            tax_ded = wages['Tax']
            tax = {'tax': tax_ded}
            wages.update(tax)
            
            rent_ded = wages['Rent']
            rent = {'rent': rent_ded}
            wages.update(rent)

            
            over_ded = wages['Over Payment']
            over = {'over': over_ded}
            wages.update(over)

            
            pension_ded = wages['Pension']
            pension = {'pension': pension_ded}
            wages.update(pension)

            
            nhf_ded = wages['NHF']
            nhf = {'nhf': nhf_ded}
            wages.update(nhf)

            
            ctls_ded = wages['CTLS']
            ctls = {'ctls': ctls_ded}
            wages.update(ctls)

            
            nhis_ded = wages['NHIS']
            nhis = {'nhis': nhis_ded}
            wages.update(nhis)

            
            salary_ded = wages['Salary Advance']
            salary = {'salary': salary_ded}
            wages.update(salary)

            
            motor_ded = wages['Motor Vehicle Advance']
            motor = {'motor': motor_ded}
            wages.update(motor)
            
            motor_alw = wages['Motor Maintainance and Fueling']
            motor_allw = {'motor_allw': motor_alw}
            wages.update(motor_allw)
            
            entertainment_alw = wages['Entertainment']
            entertainment = {'entertainment': entertainment_alw}
            wages.update(entertainment)
            
            fghb_ded = wages['FGHB']
            fghb = {'fghb': fghb_ded}
            wages.update(fghb)

            
            other_ded = wages['Other Deduction']
            other = {'other': other_ded}
            wages.update(other)
            
            personal_ded = wages['Personal Advance']
            personal = {'personal': personal_ded}
            wages.update(personal)

            basic_alw = wages['Basic']
            basic = {'basic': basic_alw}
            wages.update(basic)

            consolidated_alw = wages['total_basic_salary'] + wages['total_allowance']
            consolidated = {'consolidated': consolidated_alw}
            wages.update(consolidated)
            
            emoluments = wages['consolidated'] - wages['deductions']
            net_emolument = {'net_emoluments':emoluments}
            wages.update(net_emolument)
            
            overtime_alw = wages['Overtime']
            overtime = {'overtime': overtime_alw}
            wages.update(overtime)
            
            housing_alw = wages['Housing']
            housing = {'housing': housing_alw}
            wages.update(housing)
            
            transport_alw = wages['Transport']
            transport = {'transport': transport_alw}
            wages.update(transport)
            
            meal_alw = wages['Meal']
            meal = {'meal': meal_alw}
            wages.update(meal)
            
            utilities_alw = wages['Utilities']
            utilities = {'utilities': utilities_alw}
            wages.update(utilities)
            
            furniture_alw = wages['Furniture']
            furniture = {'furniture': furniture_alw}
            wages.update(furniture)
            
            domestic_alw = wages['Domestic Staff']
            domestic = {'domestic': domestic_alw}
            wages.update(domestic)
            
            accomodation_alw = wages['Accomodation']
            accomodation = {'accomodation': accomodation_alw}
            wages.update(accomodation) 
            
            personal_alw = wages['Personal Assistant']
            personal_allw = {'personal_alw': personal_alw}
            wages.update(personal_allw)
            
            arrear_alw = wages['Arrears']
            arrear = {'arrear': arrear_alw}
            wages.update(arrear) 
            
            newspaper_alw = wages['Newspaper']
            newspaper = {'newspaper': newspaper_alw}
            wages.update(newspaper)
            
            arrear_wage = wages['Arrear Allowance']
            arrear_allw = {'arrear_allowance': arrear_wage}
            wages.update(arrear_allw)
            
            leave_alw = wages['Leave Grant']
            leave = {'leave': leave_alw}
            wages.update(leave)
            
            under_payment_alw = wages['Under Payment']
            under_payment = {'under_payment': under_payment_alw}
            wages.update(under_payment)
            
            peculiar_alw = wages['Peculiar Allowances']
            peculiar = {'peculiar': peculiar_alw}
            wages.update(peculiar)
        return wages

    def get_year_month(self, obj):
        date = datetime.strptime(obj.date_from, '%Y-%m-%d')
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
                return value
        
report_sxw.report_sxw('report.payslip.report.march', 'hr.payslip',
                       'payslip_report/report/report_payslip_march.mako',
                        parser=payslip_march_report, header=False)
                        
                        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
