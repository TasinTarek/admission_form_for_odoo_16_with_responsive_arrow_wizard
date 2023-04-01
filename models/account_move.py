# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Invoices"

    is_admission_applicant_invoice = fields.Boolean(string="Is Admission Applicant Invoice", default=False)
    applicant_id = fields.Many2one(comodel_name="se.applicant", string="Admission Application")
    is_admission_fee_allow_payment_amount = fields.Boolean(string="Is Allow Payment Amount?", default=False)
    admission_fee_allow_payment_amount = fields.Float(string='Admission Fee Allow Amount')
    admission_fee_invoice_payment_state_allow = fields.Selection(
        [
            ('not_paid', 'Not Paid'),
            ('partially_paid', 'Partially Paid'),
            ('paid', 'Paid'),
        ],
        string='Payment Status (Based on Allow Amount)',
        default='not_paid'
    )


    def write(self, vals):
        if 'amount_residual' in vals.keys():
            if not vals['amount_residual']:
                amount_total = float(self.amount_total)
                amount_residual = float(vals['amount_residual'])
                amount_paid = float(amount_total - amount_residual)
                amount_allow_payment = float(self.admission_fee_allow_payment_amount)
        
                if self.is_admission_fee_allow_payment_amount:
                    if amount_paid >= amount_allow_payment and amount_paid < amount_total:
                        vals['admission_fee_invoice_payment_state_allow'] = 'partially_paid'
                    elif amount_paid >= amount_total:
                        vals['admission_fee_invoice_payment_state_allow'] = 'paid'
                else:
                    if amount_paid > 0 and amount_paid < amount_total:
                        vals['admission_fee_invoice_payment_state_allow'] = 'partially_paid'
                    elif amount_paid >= amount_total:
                        vals['admission_fee_invoice_payment_state_allow'] = 'paid'
        
        res = super(AccountMove, self).write(vals)
        return res

