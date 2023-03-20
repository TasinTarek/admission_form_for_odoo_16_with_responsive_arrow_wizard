# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, except_orm, UserError
import calendar
import math
import re


class SeAdmissionBoardResultGeneral(models.Model):
    _name = "se.applicant.board.result.general"
    _description = 'Admission Board Results (General Medium)'
    _rec_name = 'exam_name_ref'

    subject_name = fields.Char(string='Subject Name')
    subject_code = fields.Char(string='Subject Code')
    grade = fields.Char(string='Grade')
    
    exam_name_ref = fields.Char(string='Exam')
    educational_board = fields.Char(string='Educational Board')
    roll_number = fields.Char(string='Roll No.')
    registration_number = fields.Char(string='Registration No.')
    passing_year = fields.Char(string='Passing Year')

    applicant_id = fields.Many2one('se.applicant', string='Admission Application')


class SeAdmissionBoardResultEnglish(models.Model):
    _name = "se.applicant.board.result.english"
    _description = 'Admission Board Results (English Medium)'
    _rec_name = 'exam_name_ref'

    # exam_name_ref = fields.Char(string='Exam')
    exam_name_ref = fields.Selection(
        [
            ('o_level', 'O-Level'),
            ('a_level', 'A-Level'),
        ],
        string='Exam',
        stored=True
    )
    subject_id = fields.Many2one('se.subject', string='Subject', domain=['|', '&', ('admission_form_subject_type', '=', 'o_level'), ('admission_form_subject_type','=','a_level'),('is_allow_admission_form','=',True)])
    extra_subject_id = fields.Many2one('se.subject.extra', string='Subject')
    grade = fields.Char(string='Grade')
    
    applicant_id = fields.Many2one('se.applicant', string='Admission Application')


class SeAdmissionBoardResultAll(models.Model):
    _name = "se.applicant.board.result.all"
    _description = 'Admission Board Results'
    _rec_name = 'exam_name_ref'

    # exam_name_ref = fields.Char(string='Exam')
    exam_name_ref = fields.Selection(
        [
            ('ssc', 'SSC/Equivalent'),
            ('hsc', 'HSC/Equivalent'),
            ('o_level', 'O-Level'),
            ('a_level', 'A-Level'),
            ('o_level_equivalent', 'O-Level/Secondary/Lower Secondary/Equivalent'),
            ('a_level_equivalent', 'A-Level/Higher Secondary/12 Class Passed/Equivalent'),
            ('diploma', 'Diploma'),
            ('bachelor', 'Bachelor/Equivalent'),
            ('masters', 'Masters/Equivalent'),
            ('others', 'Others'),
        ], string='Exam', stored=True)
    institution_name = fields.Char(string='Institution Name')
    educational_board_id = fields.Many2one('se.education.board', string='Educational Board',
        domain=[
            '|','|','|','|','|','|',
            ('is_allow_for_ssc','=',True),
            ('is_allow_for_hsc','=',True),
            ('is_allow_for_o_level','=',True),
            ('is_allow_for_a_level','=',True),
            ('is_allow_for_diploma','=',True),
            ('is_allow_for_bachelors','=',True),
            ('is_allow_for_masters','=',True),
        ]
    )
    group_or_major = fields.Char(string='Group/Major')
    grade = fields.Selection(
        [
            ('first_division', '1st Division'),
            ('second_division', '2nd Division'),
            ('pass', 'Pass'),
            ('gpa', 'GPA'),
            ('others', 'Others'),
        ],
        string='Grade',
        stored=True
    )
    grade_point = fields.Float(string='Grade Point')
    result = fields.Char(string='Result')
    total_mark = fields.Float(string='Total Mark')
    # passing_year = fields.Selection(lambda self: self._get_years(), string='Passing Year', stored=True)
    passing_year = fields.Char(string='Passing Year')
    duration_year = fields.Selection(
        [
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        ],
        string='Duration Year',
        stored=True
    )
    admission_board_result_marksheet = fields.Binary(string='Marksheet', attachment=True, store=True, help="Attach all the Academic Marksheet as PDF/JPG/JPEG.")
    admission_board_result_certificate = fields.Binary(string='Certificate', attachment=True, store=True, help="Attach all the Academic Certificate as PDF/JPG/JPEG.")
    applicant_id = fields.Many2one('se.applicant', string='Admission Application')


    def _get_years(self):
        year_list = []
        
        ## Static Year Range
        # current_year = int(datetime.now().year)
        # for i in range(current_year - 10, current_year + 11):
        #     year_list.append((str(i), str(i)))

        ## Configuration Year Range
        openeducat_admission_year_range_start = self.env['ir.config_parameter'].sudo().get_param('openeducat_admission.year_range_start')
        openeducat_admission_year_range_end = self.env['ir.config_parameter'].sudo().get_param('openeducat_admission.year_range_end')
        for i in range(int(openeducat_admission_year_range_start), int(openeducat_admission_year_range_end) + 1):
            year_list.append((str(i), str(i)))
        
        return year_list

