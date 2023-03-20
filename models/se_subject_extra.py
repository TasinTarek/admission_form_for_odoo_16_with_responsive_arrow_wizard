# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class SeSubjectExtra(models.Model):
    _inherit = ['mail.thread']
    _name = 'se.subject.extra'
    _description = "Extra Subjects"

    name = fields.Char(string='Name', required=True, track_visibility='onchange')
    code = fields.Char(string='Code', readonly=True)
    # company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    note = fields.Text(string='Note')
    active = fields.Boolean(string='Active', default=True)
    admission_form_subject_type = fields.Selection([
        ('o_level', 'O-Level'),
        ('a_level', 'A-Level')
    ], string='Admission Subject Type', required=True, track_visibility='onchange')

    _sql_constraints = [
        ('name_unique', 'check(1=1)', 'No Error.'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('se.subject.extra')
        res = super(SeSubjectExtra, self).create(vals)
        return res

