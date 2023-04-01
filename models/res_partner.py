# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Partners"

    is_admission_applicant = fields.Boolean(string="Is Admission Applicant", default=False)
    # applicant_id = fields.Many2one(comodel_name="op.admission", string="Admission Application")
    applicant_ids = fields.One2many(comodel_name="op.admission", inverse_name='partner_id', string="Admission Applications")

