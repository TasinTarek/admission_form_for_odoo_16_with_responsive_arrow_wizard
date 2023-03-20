# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class SeSubject(models.Model):
    _name = 'se.subject'
    _description = "Subjects"

    is_allow_admission_form = fields.Boolean(string="Allow Admission Form", default=False)
    admission_form_subject_type = fields.Selection([
        ('o_level', 'O-Level'),
        ('a_level', 'A-Level'),
    ], string='Admission Subject Type')


    @api.model
    def create(self, vals):
        if 'is_allow_admission_form' in vals.keys():
            if not vals['is_allow_admission_form']:
                vals['admission_form_subject_type'] = ''
        
        res = super(SeSubject, self).create(vals)
        return res


    def write(self, vals):
        if 'is_allow_admission_form' in vals.keys():
            if not vals['is_allow_admission_form']:
                vals['admission_form_subject_type'] = ''
        
        res = super(SeSubject, self).write(vals)
        return res

