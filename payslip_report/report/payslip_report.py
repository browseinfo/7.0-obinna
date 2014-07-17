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

class payslip_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(payslip_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_payslip_lines':self.get_payslip_lines,
            'get_year_month': self.get_year_month,
        })

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
            allowance = (wages['Housing'] + wages['Transport'] + wages['Meal'] + wages['Utilities'] + wages['Furniture'] + wages['Domestic Staff'] + wages['Leave Grant'])
            total_allowance = {'allowance' : allowance}
            wages.update(total_allowance)

            deductions = (wages['Tax'] + wages['Rent'] + wages['Over Payment'] + wages['Pension'] + wages['NHF'] + wages['CTLS'] + wages['NHIS'] + wages['Salary Advance'] + wages['Motor Vehicle Advance'] + wages['FGHB'] + wages['Other Deduction'] + wages['Personal Advance'])
            total_deductions = {'deductions': deductions}
            wages.update(total_deductions)

            emolument = (wages['Basic'] + wages['allowance'])
            gross_emolument = {'emolument':emolument}
            wages.update(gross_emolument)

            emoluments = (wages ['emolument'] - wages['deductions'])
            net_emolument = {'emoluments':emoluments}
            wages.update(net_emolument)
        return wages

    def get_year_month(self, date):
        month = {'01':'JANUARY',
                 '02':'FEBRUARY',
                 '03':'MARCH',
                 '04':'APRIL',
                 '05':'MAY',
                 '06':'JUNE',
                 '07':'JULY',
                 '08':'AUGUST',
                 '09':'SEPTEMBER',
                 '10':'OCTOBER',
                 '11':'NOVEMBER',
                 '12':'DECEMBER',
                }
        dt = date.split('-')
        for key, value in month.iteritems():
            if key == dt[1]:
                return value
        
report_sxw.report_sxw('report.payslip.report', 'hr.payslip',
                       'payslip_report/report/report_payslip.rml',
                        parser=payslip_report, header=False)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
