# -*- coding: utf-8 -*-
import time
from datetime import datetime
from dateutil import relativedelta
from openerp.exceptions import UserError
from openerp import models, fields, api, _

class InsuranceConfiguration(models.Model):
    _name = 'insurance.configuration'


    name = fields.Char(string="Name")
    max_limit = fields.Float(string="Max Limit")
    year = fields.Selection(
        [(num, str(num)) for num in range(((datetime.now().year) - 5), ((datetime.now().year) + 5))])
    insurance_wage_type = fields.Selection([('variable_insurance_limit', 'Variable Insurance Limit'), ('fixed_insurance_limit', 'Fixed Insurance Limit')],string="Insurance Wage Type")
    employee_ratio = fields.Float(string="Employee Ratio (%)")
    company_ratio = fields.Float(string="Company Ratio (%)")

    @api.onchange('insurance_wage_type')
    def onchange_insurance_wage_type(self):
        if self.insurance_wage_type == 'fixed_insurance_limit':
            self.employee_ratio = 14.00
            self.company_ratio = 26.00
        elif self.insurance_wage_type == 'variable_insurance_limit':
            self.employee_ratio = 11.00
            self.company_ratio = 24.00
        else:
            self.employee_ratio = 00.00
            self.company_ratio = 00.00