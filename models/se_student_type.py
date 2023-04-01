# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class OpStudentType(models.Model):
    _inherit = ['mail.thread']
    _name = "se.student.type"
    _description = 'Student Types'

    name = fields.Char(string='Name', required=True, track_visibility='onchange')
    code = fields.Char(string='Code', readonly=True)
    student_type_code = fields.Char(string='Student Type Code', track_visibility='onchange')
    # company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.user.company_id.id)
    # currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    note = fields.Text(string='Note')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('done', 'Confirmed'),
            ('cancel', 'Canceled'),
        ],
        string='State',
        default='draft',
        track_visibility='onchange',
        store=True
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
        ('student_type_code_unique', 'unique(student_type_code)', 'Student Type Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('op.student.type')
        res = super(OpStudentType, self).create(vals)
        return res

    # def unlink(self):
    #     for line in self:
    #         if line.state == 'done':
    #             raise UserError("You cannot delete an entry which has been validated.")
    #     res = super(OpPaymentCategory, self).unlink()
    #     return res

    def action_validate(self):
        for line in self:
            line.state = 'done'

    def action_cancel(self):
        for line in self:
            line.state = 'draft'

