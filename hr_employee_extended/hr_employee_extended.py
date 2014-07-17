# -*- coding: utf-8 -*-
##############################################################################
#
#    Sales and Account Invoice Discount Management
#    Copyright (C) 2013-2014 BrowseInfo(<http://www.browseinfo.in>).
#    
##############################################################################

from osv import osv,fields
import psycopg2
from openerp import netsvc
import base64
import cStringIO
import csv
import urllib
import binascii
import tools
from tools import ustr
from datetime import date
import os
import datetime
import time
from openerp.osv import fields,osv
from openerp.tools.translate import _

class hr_employee(osv.Model):
    _inherit="hr.employee"  
    
    '''def arrear_update(self, cr, uid, ids, context=None):
        res = {}  
        if context is None:
            context = {}
        if not ids:
            ids = self.search(cr, uid, [])
        res = {}.fromkeys(ids, 0.0)
        if not ids:
            return res 

        current_obj = self.browse(cr, uid, ids, context=context)[0]
        total_arrear = (current_obj.rank_id.peculiar + current_obj.rank_id.leave_grant) * 2
        
        return self.write(cr, uid, current_obj.id, {'arrear_allow': total_arrear})'''    
        
    _columns={
	    'file_number':fields.char("File No"),
	    'title':fields.char("Title"),
	    'state_of_origin':fields.many2one('res.country.state',"State Of Origin"),
	    'local_goverment_area':fields.char("Local Government Area"),
	    'qualification':fields.char("Qualification"),
	    'station_deployed':fields.char("Station Deployed"),
	    'date_of_appointment':fields.date("Date Of First Appointment"),
	    'date_of_present_appointment':fields.date("Date Of Present Appointment"),
	    'rank_id':fields.many2one('grade.step',"Rank"),
	    'new_staff':fields.boolean("New Staff"),
	    'bank_name':fields.many2one('res.partner.bank',"Bank Name"),
	    'bank_pay_point':fields.many2one('bank.pay.point',"Bank Pay Point"),
	    'bank_account_number':fields.integer("Bank Account Number"),
	    'tin_number':fields.integer("Tin Number"),
        'ctls': fields.float('CTLS', digits=(16,2)),
        'underpayment': fields.float('Under Payment', digits=(16,2)),
        'arrears_basic': fields.float('Arrears Basic', digits=(16,2)),
        'over_payment': fields.float('Over Payment', digits=(16,2)),
        'nhis': fields.float('NHIS', digits=(16,2)),
        'salary_advance': fields.float('Salary Advance', digits=(16,2)),
        'motor_advance': fields.float('Motor Vehicle Advance', digits=(16,2)),
        'fghb': fields.float('FGHB', digits=(16,2)),
        'other_deduction': fields.float('Other Deduction', digits=(16,2)),
        'personal_advance': fields.float('Personal Advance', digits=(16,2)),
        'arrear_allow': fields.float('Arrear Allowance', digits=(16,2)),
        'overtime': fields.float('Overtime', digits=(16,2)),
	}
	
	
	
                
hr_employee()

class res_partner_bank(osv.Model):
    _inherit="res.partner.bank"
    _columns = {
        'sort_code':fields.char("Sort Code"),
        'branch_code':fields.char("Branch Code"),
        'account_type': fields.char('Account Type'),
        'acc_unit': fields.char('BENEFICIARY ACCOAREA 11UNT'),
    }

res_partner_bank()

class grade(osv.Model):
    _name = 'grade'
    _columns = {
        'name': fields.char('Grade')
    }

grade()

class step(osv.Model):
    _name = 'step'
    _columns = {
        'name': fields.char('Step')
    }

step()
    
class grade_step(osv.Model):

    def name_get(self, cr, uid, ids, context=None):
        result= []
        if not all(ids):
            return result
        for pl in self.browse(cr, uid, ids, context=context):
            rank = pl.grade_id.name +  ' - '+pl.step_id.name
            result.append((pl.id,rank))
        return result

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        ids = self.search(cr, user, [('grade_id.name', operator, name)]+ args, limit=limit, context=context)
        ids += self.search(cr, user, [('step_id.name', operator, name)]+ args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context)


    _name = 'grade.step'
    _columns = {
        'grade_id': fields.many2one('grade', 'Grade'),
        'step_id': fields.many2one('step', 'Step'),
        'wage': fields.float('Wage', digits=(16,2)),
        'tax_annum': fields.float('Tax Per Annum', digits=(16,2)),
        'tax_month': fields.float('Tax Per Month', digits=(16,2)),
        'housing': fields.float('Housing', digits=(16,2)),
        'transport': fields.float('Transport', digits=(16,2)),
        'utility': fields.float('Utility', digits=(16,2)),
        'furniture': fields.float('Furniture', digits=(16,2)),
        'meal': fields.float('Meal', digits=(16,2)),
        'domestic': fields.float('Domestic Servants', digits=(16,2)),
        'leave_grant': fields.float('Leave Grant', digits=(16,2)),
        'peculiar': fields.float('Peculiar', digits=(16,2)),
        'consolidated': fields.float('Consolidated', digits=(16,2)),
        'accomodation': fields.float('Accomodation', digits=(16,2)),
        'entertainment': fields.float('Entertainment', digits=(16,2)),
        'motor': fields.float('Motor Maintainance & Fueling', digits=(16,2)),
        'newspaper': fields.float('Newspaper', digits=(16,2)),
        'personal_assistant': fields.float('Personal Assistant', digits=(16,2)),

    }
    def write(self, cr, uid, ids, vals, context=None):
        employe_obj = self.pool.get('hr.employee')
        contract_obj = self.pool.get('hr.contract')
        employe_ids = employe_obj.search(cr, uid, [('rank_id','=',ids)], context=context)
        contract_ids = contract_obj.search(cr, uid, [('employee_id','=',employe_ids)], context=context)
        contract_obj.write(cr, uid, contract_ids, vals, context=context)
        return super(grade_step, self).write(cr, uid, ids, vals, context=context)
        
grade_step()
    	
class res_rank(osv.Model):
    _name="res.rank"
    _columns={
        'name':fields.char("Name",required=True),
        'description':fields.text("Description"),
    }

res_rank()

class bank_pay_point(osv.Model):
    _name="bank.pay.point"
    _columns={
        'name':fields.char("Name",required=True),
        'description':fields.text("Description"),
    }

bank_pay_point()

class hr_contract(osv.Model):
    _inherit="hr.contract"
    _columns={
        'tax_annum': fields.float('Tax Per Annum', digits=(16,2)),
        'tax_month': fields.float('Tax Per Month', digits=(16,2)),
        'housing': fields.float('Housing', digits=(16,2)),
        'transport': fields.float('Transport', digits=(16,2)),
        'utility': fields.float('Utility', digits=(16,2)),
        'furniture': fields.float('Furniture', digits=(16,2)),
        'meal': fields.float('Meal', digits=(16,2)),
        'domestic': fields.float('Domestic Servants', digits=(16,2)),
        'leave_grant': fields.float('Leave Grant', digits=(16,2)),
        'peculiar': fields.float('Peculiar', digits=(16,2)),
        'consolidated': fields.float('Consolidated', digits=(16,2)),
        'accomodation': fields.float('Accomodation', digits=(16,2)),
        'entertainment': fields.float('Entertainment', digits=(16,2)),
        'motor': fields.float('Motor Maintainance & Fueling', digits=(16,2)),
        'newspaper': fields.float('Newspaper', digits=(16,2)),
        'personal_assistant': fields.float('Personal Assistant', digits=(16,2)),
    }

    def on_change_employee(self, cr, uid, ids, employee_id, context=None):
        context = context or {}
        res = {}
        if employee_id:
            employee_obj = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
            if employee_obj and employee_obj.rank_id:
                res['wage'] = (employee_obj.rank_id.wage)
                res['tax_annum'] = employee_obj.rank_id.tax_annum
                res['tax_month'] = employee_obj.rank_id.tax_month
                res['housing'] = employee_obj.rank_id.housing
                res['furniture'] = employee_obj.rank_id.furniture
                res['meal'] = employee_obj.rank_id.meal
                res['domestic'] = employee_obj.rank_id.domestic
                res['leave_grant'] = employee_obj.rank_id.leave_grant
                res['peculiar'] = employee_obj.rank_id.peculiar
                res['consolidated'] = employee_obj.rank_id.consolidated
                res['accomodation'] = employee_obj.rank_id.accomodation
                res['entertainment'] = employee_obj.rank_id.entertainment
                res['motor'] = employee_obj.rank_id.motor
                res['newspaper'] = employee_obj.rank_id.newspaper
                res['personal_assistant'] = employee_obj.rank_id.personal_assistant
                res['utility'] = employee_obj.rank_id.utility
                res['transport'] = employee_obj.rank_id.transport
            else:
                res['wage'] = 0.00
                res['tax_annum'] = 0.00
                res['tax_month'] = 0.00 
                res['housing'] = 0.00
                res['furniture'] = 0.00
                res['meal'] = 0.00
                res['domestic'] = 0.00
                res['leave_grant'] = 0.00
                res['peculiar'] = 0.00
                res['consolidated'] = 0.00
                res['accomodation'] = 0.00
                res['entertainment'] = 0.00
                res['motor'] = 0.00
                res['newspaper'] = 0.00
                res['personal_assistant'] = 0.00
                res['utility'] = 0.00
                res['transport'] = 0.00
        return {'value': res}
    
hr_contract()
	
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
