# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class OpCourse(models.Model):
    _inherit = 'se.course'
    _description = "Courses"

    is_local_bachelor_program_hsc = fields.Boolean(string='Local - Bachelor Program - HSC', default=False)
    is_local_bachelor_program_a_level = fields.Boolean(string='Local - Bachelor Program - A-Level', default=False)
    is_local_bachelor_program_diploma = fields.Boolean(string='Local - Bachelor Program - Diploma', default=False)
    is_local_masters_program_bachelor = fields.Boolean(string='Local - Masters Program - Bachelor', default=False)
    is_international_bachelor_program = fields.Boolean(string='International - Bachelor Program', default=False)
    is_international_masters_program = fields.Boolean(string='International - Masters Program', default=False)
    # campus_ids = fields.Many2many(comodel_name='op.campus.facility', string='Campus', domain=[('is_campus','=',True)])
    admission_eligibility = fields.Text(string='Eligibility')

