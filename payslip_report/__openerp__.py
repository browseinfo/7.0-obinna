# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2014 BrowseInfo (<http://www.browseinfo.in>).
#
##############################################################################

{
    'name':' Employee Payslip Report',
    'version':'7.0',
    'author':'BrowseInfo',
    'website':'http://www.browseinfo.in',
    'images':[],
    'data': [
            'data.xml',
            'payslip_report.xml',
            ],
    'depends':['hr_payroll','hr_employee_extended', 'report_webkit'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

