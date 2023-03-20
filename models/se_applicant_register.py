# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SeAdmissionRegister(models.Model):
    _name = 'se.applicant.register'
    _inherit = "mail.thread"
    _description = 'Admission Register'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    course_id = fields.Char(string='Course')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    course_fees = fields.Char(string='Course Fees')
    min_count = fields.Integer(string='Minimum No. of Admission')
    max_count = fields.Integer(string='Max No. of Admission')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
        ('application', 'Application Gathering'),
        ('admission', 'Admission Process'),
        ('done', 'Done')
    ], string='Status', default='draft', track_visibility='onchange')
    applicant_ids = fields.One2many(comodel_name='se.applicant',
                                    inverse_name='register_id',
                                    string='Admissions')

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = fields.Date.from_string(record.end_date)
            if start_date > end_date:
                raise ValidationError("End Date cannot be set before Start Date.")

    @api.constrains('min_count', 'max_count')
    def check_no_of_admission(self):
        for record in self:
            if (record.min_count < 0) or (record.max_count < 0):
                raise ValidationError(
                    _("No of Admission should be positive!"))
            if record.min_count > record.max_count:
                raise ValidationError("Min Admission can't be greater than Max Admission")

    def confirm_register(self):
        self.state = 'confirm'

    def set_to_draft(self):
        self.state = 'draft'

    def cancel_register(self):
        self.state = 'cancel'

    def start_application(self):
        self.state = 'application'

    def start_admission(self):
        self.state = 'admission'

    def close_register(self):
        self.state = 'done'


