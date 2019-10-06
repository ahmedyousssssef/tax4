# -*- coding: utf-8 -*-
from __future__ import division
from openerp import models, fields, api

class SalaryTax(models.Model):
    _inherit = 'hr.payslip'


    tax_rule_ids = fields.Many2many(comodel_name="salary.tax.rule",string="Tax Computation",relation='hr_tax_rule_rel',compute='_onchange_tax_employee_id')
    tax_amount = fields.Float(string="Tax Amount",  required=False, )
    payslip_tax_type = fields.Selection(string="Tax Type", help="Compute Tax For Employee On Payslip",
                                        selection=[('annual', 'Annually'), ('month', 'Monthly'), ], required=False,default='month')

    @api.one
    @api.depends('employee_id')
    def _onchange_tax_employee_id(self):
        taxes = self.pool.get('salary.tax.rule').search([]).ids
        self.tax_rule_ids = taxes

    # def compute_sheet(self, cr, uid, ids, context=None):
    #     slip_line_pool = self.pool.get('hr.payslip.line')
    #     sequence_obj = self.pool.get('ir.sequence')
    #     for payslip in self.browse(cr, uid, ids, context=context):
    #         number = payslip.number or sequence_obj.next_by_code(cr, uid, 'salary.slip')
    #         # delete old payslip lines
    #         old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
    #         #            old_slipline_ids
    #         if old_slipline_ids:
    #             slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
    #         if payslip.contract_id:
    #             # set the list of contract for which the rules have to be applied
    #             contract_ids = [payslip.contract_id.id]
    #         else:
    #             # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
    #             contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to,
    #                                              context=context)
    #         lines = [(0, 0, line) for line in
    #                  self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id,
    #                                                                context=context)]
    #         self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number, }, context=context)
    #     return True

    # @api.multi
    def compute_sheet(self, cr, uid, ids, context=None):
        tot_amount = 0.0
        total_tax = 0.0
        total_discount = 0.0

        for payslip in self.browse(cr, uid, ids, context=context):
            number = payslip.number or self.pool.get('ir.sequence').next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or \
                           self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to,
                                                 context=context)
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            print(lines , "linnnnnneeeeessss")
            for line in lines:
                print(line[2]['salary_rule_id'] , "llllllllllll")
                # rule_data = self.env['hr.salary.rule'].search(cr, uid, [line[2]['salary_rule_id']], context=context)
                rule_data = self.pool.get('hr.salary.rule').browse(cr, uid, [line[2]['salary_rule_id']], context=context)
                if rule_data.taxable:
                    tot_rule = float(line[2]['amount']) * float(line[2]['quantity']) * float(line[2]['rate']) / 100.0
                    tot_amount += tot_rule
            # print(self.pool.get('res.currency').browse(cr, uid, self.pool.get('res.currency').search(cr, uid, [('name', '=', 'EGP')], context=context), context=context).rate , "mmlkmlm")
            tot_amount = tot_amount * (self.pool.get('res.currency').browse(cr, uid, self.pool.get('res.currency').search(cr, uid, [('name', '=', 'EGP')], context=context), context=context).rate)
            tot_amount = tot_amount * 12
            if tot_amount:
                tot_amount = tot_amount - payslip.tax_rule_ids[0].ex_limit
                for line in payslip.tax_rule_ids:
                    if not line.level == str(len(payslip.tax_rule_ids)):
                        if tot_amount > (line.amount_to - line.amount_from):
                            total_tax += line.total_tax
                            tot_amount -= (line.amount_to - line.amount_from)

                        elif tot_amount <= (line.amount_to - line.amount_from):
                            tax_level = tot_amount * (line.tax_rate / 100)
                            total_tax += tax_level
                            total_discount = total_tax * (line.tax_exemption / 100)
                            break
                        else:
                            if tot_amount < line.amount_from:
                                tax_level = tot_amount * (line.tax_rate / 100)
                                total_tax += tax_level
                                total_discount = total_tax * (line.tax_exemption / 100)
                                break
                    else:
                        tax_level = tot_amount * (line.tax_rate / 100)
                        total_tax += tax_level
                        total_discount = total_tax * (line.tax_exemption / 100)
                        break

            tax_amount = total_tax - total_discount
            taxes = self.pool.get('hr.payroll.config.settings').search(cr, uid, [] , context=context)

            if taxes:
                for tax in taxes[-1]:
                    if tax.payslip_tax_type == 'month':
                        payslip.write({'tax_amount': round(tax_amount / self.pool.get('res.currency').browse(cr, uid, self.pool.get('res.currency').search(cr, uid, [('name', '=', 'EGP')], context=context), context=context).rate /12), 'payslip_tax_type': 'month'})
                    else:
                        payslip.write({'tax_amount': round(tax_amount), 'payslip_tax_type': 'annual'})
            else:
                payslip.write({'tax_amount': round(tax_amount / self.pool.get('res.currency').browse(cr, uid, self.pool.get('res.currency').search(cr, uid, [('name', '=', 'EGP')], context=context), context=context).rate /12), 'payslip_tax_type': 'month'})

            payslip.write({'line_ids': lines, 'number': number, })
        return super(SalaryTax,self).compute_sheet(cr, uid, ids, context)

