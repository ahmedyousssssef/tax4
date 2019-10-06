# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from datetime import datetime
from dateutil import relativedelta
from openerp.exceptions import ValidationError

class AllowanceLine(models.Model):
    _name = "allowance.line"

    name = fields.Char(string="Name")
    value = fields.Float(string="Value")
    contract = fields.Many2one('hr.contract' , string="Contract")




class hr_contract_inherit(models.Model):
    _inherit = 'hr.contract'

    is_insured = fields.Boolean(string="Is Insured ?" , default=False)

    allowance_line = fields.One2many('allowance.line','contract' , string="Allowances")
