# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re
import requests
import json


class SeAdmissionAchievement(models.Model):
    _name = "se.applicant.achievement"
    _description = 'Admission Applicant Achievements'

    name = fields.Char(string='Title')
    year = fields.Char(string='Year')

    applicant_id = fields.Many2one('se.applicant', string='Admission Application')


class SeAdmissionProfessionalExperience(models.Model):
    _name = "se.applicant.professional.experience"
    _description = 'Admission Applicant Professional Experiences'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    duration = fields.Char(string='Duration')
    annual_income = fields.Float(string='Annual Income', default=0)
    professional_experience_certificate = fields.Binary(string='Certificate', attachment=True, store=True, help="Attach all the Professional Experience Certificate as PDF/JPG/JPEG.")
    applicant_id = fields.Many2one('se.applicant', string='Admission Application')

