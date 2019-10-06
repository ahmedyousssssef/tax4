# -*- coding: utf-8 -*-

from openerp import models, fields, api , _
from datetime import datetime,timedelta,date

import time
from dateutil import relativedelta


class EmployeeAllowance(models.Model):
    _name = "employee.allowance"

    user_id = fields.Many2one('res.users', index=True, track_visibility='onchange',  compute='_get_current_user')
    # department_manger = fields.Many2one(string='Department Manager' , related='department_id.manager_id')
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    department_id = fields.Many2one('hr.department', 'Department')
    date_from = fields.Date(string='Date From',required=True,
        default=time.strftime('%Y-%m-01'), )
    date_to = fields.Date(string='Date To',required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],)
    all_allowanses = fields.Selection([('allowanse1' , 'allowanse1'),('allowanse2' , 'allowanse2')],string='Allowanse')
    allowanse_type = fields.Selection([('amount' , 'Amount'),('percent' , 'Percentage')],string='Allowanse Type')
    percent = fields.Float(string='Percentage')
    value = fields.Float(string='Amount')
    reason = fields.Text(string='Reason',  required=True)

    department_manager_usr = fields.Boolean(compute='check_dep_man_usr')




    state = fields.Selection([
        ('draft', 'New'),
        ('dep_man', 'Department Manager Approved'),
        ('gen_man', 'General Manager Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status',
       track_visibility='onchange', help='Status of the punishment', default='draft')


    @api.depends()
    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user
        # i think this work too so you don't have to loop
        self.write({'current_user' : self.env.user.id})


    @api.onchange('allowanse_type' , 'percent' , 'employee_id')
    def get_percent_value(self):
        if self.employee_id and self.allowanse_type == 'percent':
            contract_wage = self.employee_id.contract_id.wage
            self.value = (contract_wage * self.percent)/100

    @api.onchange('employee_id')
    def get_employee_department(self):
        department = self.employee_id.department_id
        if self.department_id == False or self.department_id.id != department.id:
            self.department_id = department

    @api.onchange('department_id')
    def get_department_employees(self):
        if self.department_id:
            emps = []
            for emp in self.env['hr.employee'].search([('department_id' , '=' , self.department_id.id)]):
                emps.append(emp.id)
            return {
                'domain': {
                    'employee_id': [('id', 'in', emps)]
                }}

    @api.depends('department_id' , 'user_id')
    def check_dep_man_usr(self):
        print(self.env.user.id , self.department_id.manager_id.user_id.id , self.state)
        if self.env.user.id == self.department_id.manager_id.user_id.id and self.state == 'draft':
            self.department_manager_usr = True
        else:
            self.department_manager_usr = False




    def department_manager_approve(self):
        self.state = 'dep_man'



    def general_manager_approve(self):
        self.state = 'gen_man'

    @api.multi
    def button_cancel(self):
        self.write({'state': 'cancel'})