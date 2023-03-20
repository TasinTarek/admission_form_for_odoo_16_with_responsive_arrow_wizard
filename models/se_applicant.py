from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
import requests
import json
import datetime

from num2words import num2words


class SeApplicant(models.Model):
    _name = 'se.applicant'
    _description = 'SmartEdu Admission'
    # _inherit = 'se.education.board'
    # _inherit =
    _inherit = ['mail.thread', 'mail.activity.mixin', 'se.education.board']
    # _inherits = {"res.partner": "partner_id"}
    # _inherit = 'res.partner'

    name = fields.Char(string='Name', compute='_compute_name_concat')
    first_name = fields.Char(string='First Name', required=True, translate=True)
    middle_name = fields.Char('Middle Name', translate=True)
    last_name = fields.Char('Last Name', required=True, translate=True)
    applicant_photo = fields.Image(string='Photo', attachment=True, store=True)
    # is_alumni = fields.Boolean(string='Is Alumni ?')
    is_student = fields.Boolean(string='Is Already Student')
    student_id = fields.Many2one(comodel_name='se.student', string='Student ID')
    register_id = fields.Many2one(comodel_name='se.applicant.register', string='Register ID')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('confirm', 'Confirmed'),
        ('admission', 'Admission Confirm'),
        ('reject', 'Rejected'),
        ('pending', 'Pending'),
        ('cancel', 'Cancelled'),
        ('done', 'Done')
    ], 'State', default='draft', track_visibility='onchange')

    # Academic Fields

    application_number = fields.Char('Application Number')
    admission_date = fields.Date('Admission Date')
    admission_expire_date = fields.Date('Admission Expire Date')
    application_date = fields.Datetime('Application Date')
    course_id = fields.Char('Course')
    curriculum_id = fields.Char('Curriculum ')
    order_id = fields.Char('Registration Fees Ref')
    batch_id = fields.Many2one(comodel_name='se.batch', string='Batch')
    application_serial_number = fields.Char('Application Serial Number')
    fees = fields.Float('Admission Form Fee')
    admission_fee = fields.Float('Admission Fee')
    fees_term_id = fields.Char('Fees Term')
    academic_faculty_id = fields.Char('Academic Faculty')
    department_id = fields.Char('Department')
    semester_year_string = fields.Date('Year')
    semester_id = fields.Char('Semester')
    semester_type_id = fields.Many2one(comodel_name='se.semester.type', string='Semester Type')
    education_shift_id = fields.Many2one(comodel_name='se.education.shift', string='Education Shift')
    # campus_id = fields.Many2one(comodel_name='se.venue', string='Campus', ondelete='restrict')
    campus_id = fields.Char(string='Campus')
    form_type = fields.Selection([
        ('local_bachelor_program_hsc', 'Local-Bachelor Program - HSC'),
        ('local_bachelor_program_a_level', 'Local-Bachelor Program - A-Level'),
        ('local_bachelor_program_diploma', 'Local-Bachelor Program - Diploma'),
        ('local_masters_program_bachelor', 'Local-Masters Program - Bachelor'),
        ('international_bachelor_program_a_level', 'International-Bachelor Program '),
        ('international_masters_program', 'International - Masters Program'),
    ], string='Apply Type', )
    student_type = fields.Selection([
        ('local', 'Local'),
        ('international', 'International')
    ], string='Student Type', )
    form_apply_type = fields.Selection([
        ('offline', 'Offline'),
        ('online', 'Online')
    ], string='Form Apply Type', default='offline', store=True)
    admission_type = fields.Selection([
        ('direct', 'Direct Admission'),
        ('online', 'Online Admission')
    ], string='Admission Type', store=True)
    academic_medium_type = fields.Selection([
        ('general', 'General'),
        ('english', 'English'),
    ], string='Academic Medium', store=True)
    campus_type = fields.Selection([
        ('on_campus', 'On Campus'),
        ('off_campus', 'Off Campus'),
    ], string='Campus Type', default='on_campus', store=True)

    eligibility_state = fields.Selection([
        ('uncheck', 'Not Verified'),
        ('approve', 'Verified'),
        ('reject', 'Rejected')
    ], string='Eligibility Status', )
    eligibility_applicant_state = fields.Selection([
        ('uncheck', 'Uncheck'),
        ('agree', 'Agree'),
        ('disagree', 'Disagree')
    ], string='Applicant Status', )
    is_eligible_for_admission_test = fields.Boolean(string='Is Eligible Admission for Test?', default=False)
    admission_test_date = fields.Datetime(string='Admission Test Date')
    # admission_test_venue_id = fields.Many2one(comodel_name='se.venue', string='Admission Test Venue')
    admission_test_venue_id = fields.Char(string='Admission Test Venue')
    result_publish_date = fields.Datetime(string='Result Publish Date')
    student_type_id = fields.Many2one(comodel_name='se.student.type', string='Student Type')

    is_credit_transfer = fields.Boolean(string='Create Transfer')
    prev_institute = fields.Char(string='Previous Institute')
    prev_course = fields.Char(string='Previous Course')
    prev_subject_completed = fields.Integer(string='Previous Completed Subject Count')
    prev_cgpa = fields.Char(string='Previous CGPA')
    prev_transcript = fields.Binary(string='Previous Transcript', attachment=True, store=True,
                                    help="Applicant Previous Transcript.")

    # SSC
    ssc_gpa = fields.Float(string='SSC GPA')
    ssc_grade = fields.Char(string='SSC Grade')
    ssc_certificate = fields.Binary(string='SSC Academic Transcript', attachment=True, store=True,
                                    help="Applicant SSC Certificate.")
    is_golden_ssc = fields.Boolean(string='Is Golden in SSC?')
    roll_number_ssc = fields.Char(string='Roll No.')
    registration_number_ssc = fields.Char(string='Reg. No.')
    year_ssc = fields.Char(string='Year', stored=True)
    education_board_ssc_id = fields.Many2one(comodel_name='se.education.board', string='Education Board')
    admission_board_result_ssc_ids = fields.One2many(comodel_name='se.applicant.board.result.general',
                                                     inverse_name='applicant_id',
                                                     string='Admission Board Results of HSC',
                                                     domain=[('exam_name_ref', '=', 'ssc')])
    is_get_educational_board_result_ssc = fields.Boolean(string='Is Get Education Board Result of SSC?', default=False,
                                                         readonly=True)

    # HSC
    hsc_gpa = fields.Float(string='HSC GPA')
    hsc_grade = fields.Char(string='HSC Grade')
    hsc_certificate = fields.Binary(string='HSC Academic Transcript', attachment=True, store=True,
                                    help="Applicant HSC Certificate.")
    is_golden_hsc = fields.Boolean(string='Is Golden in HSC?')
    roll_number_hsc = fields.Char(string='Roll No.')
    registration_number_hsc = fields.Char(string='Reg. No.')
    year_hsc = fields.Char(string='Year', stored=True)
    education_board_hsc_id = fields.Many2one(comodel_name='se.education.board', string='Education Board')
    admission_board_result_hsc_ids = fields.One2many(comodel_name='se.applicant.board.result.general',
                                                     inverse_name='applicant_id',
                                                     string='Admission Board Results of HSC',
                                                     domain=[('exam_name_ref', '=', 'hsc')])
    is_get_educational_board_result_hsc = fields.Boolean(string='Is Get Education Board Result of HSC?', default=False,
                                                         readonly=True)

    # O-level
    education_board_o_level_id = fields.Many2one(comodel_name='se.education.board', string='Exam Board',
                                                 domain=[('academic_medium_type', '=', 'english'),
                                                         ('is_allow_for_o_level', '=', True)])
    passing_year_o_level = fields.Char(string='Passing Year', stored=True)
    o_level_certificate = fields.Binary(string='O-Level Academic Transcript', attachment=True, store=True,
                                        help="Applicant O-Level Certificate.")
    admission_board_result_o_level_ids = fields.One2many(comodel_name='se.applicant.board.result.english',
                                                         inverse_name='applicant_id',
                                                         string='Admission Board Results of O-Level',
                                                         domain=[('exam_name_ref', '=', 'o_level')])

    # A-level
    education_board_a_level_id = fields.Many2one(comodel_name='se.education.board', string='Exam Board',
                                                 domain=[('academic_medium_type', '=', 'english'),
                                                         ('is_allow_for_a_level', '=', True)])
    passing_year_a_level = fields.Char(string='Passing Year', stored=True)
    a_level_certificate = fields.Binary(string='A-Level Academic Transcript', attachment=True, store=True,
                                        help="Applicant A-Level Certificate.")
    admission_board_result_a_level_ids = fields.One2many(comodel_name='se.applicant.board.result.english',
                                                         inverse_name='applicant_id',
                                                         string='Admission Board Results of A-Level',
                                                         domain=[('exam_name_ref', '=', 'a_level')])

    admission_board_result_all_certificate = fields.Binary(string='All Academic Certificate', attachment=True,
                                                           store=True,
                                                           help="Attach all the Academic Certificate in single document (PDF).")
    admission_board_result_all_ids = fields.One2many(comodel_name='se.applicant.board.result.all',
                                                     inverse_name='applicant_id',
                                                     string='Admission Board Results')

    # Achievement & Experience
    admission_achievement_ids = fields.One2many(comodel_name='se.applicant.achievement',
                                                inverse_name='applicant_id',
                                                string='Admission Applicant Achievements')
    admission_professional_experience_ids = fields.One2many(comodel_name='se.applicant.professional.experience',
                                                            inverse_name='applicant_id',
                                                            string='Admission Applicant Professional Experiences')

    # Personal Details

    signature = fields.Binary(string='Signature', attachment=True, store=True, help="Applicant signature.")
    passport = fields.Binary(string='Passport', attachment=True, store=True, help="Applicant passport.")
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], string='Gender', required=False, states={'done': [('readonly', True)]})
    birth_date = fields.Date('Birth Date', required=False, states={'done': [('readonly', True)]})
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string='Marital Status', store=True)
    email = fields.Char(string='Email')
    alternate_email = fields.Char(string='Alternate Email')
    emergency_contact_info = fields.Char(string='Emergency Contact')
    phone = fields.Char(String='Phone')
    mobile = fields.Char(String='Mobile')
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    state_id = fields.Char()
    zip = fields.Char()
    country_id = fields.Char()
    permanent_district_id = fields.Selection([
        ('dhaka', 'Dhaka'),
        ('valor2', 'valor2')
    ], string='Permanent District', )
    present_district_id = fields.Selection([
        ('dhaka', 'Dhaka'),
        ('ctg', 'CTG')
    ], string='Present District', )
    is_permanent_present_address_same = fields.Boolean(
        string='Present Address same as Permanent Address')
    present_street = fields.Char()
    present_street2 = fields.Char()
    present_city = fields.Char()
    present_state = fields.Char()
    present_zip = fields.Char()
    present_country_id = fields.Char()
    mailing_address = fields.Selection([
        ('present_address', 'Present Address'),
        ('permanent_address', 'Permanent Address'),
        ('other_address', 'Other Address'),
    ], string='Mailing Address', store=True)
    other_street = fields.Char(string='Street')
    other_street2 = fields.Char(string='Street2')
    other_city = fields.Char(string='City')
    # other_state_id = fields.Many2one(comodel_name='res.country.state', string='States')
    other_zip = fields.Char(string='Zip')
    # other_country_id = fields.Many2one(comodel_name='res.country', string='Country')
    # other_district_id = fields.Many2one(comodel_name='op.district', string='District')
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('hinduism', 'Hinduism'),
        ('christianity', 'Christianity'),
        ('buddhism', 'Buddhism'),
        ('other', 'Other'),
    ], string='Religion', store=True)
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group', store=True)
    whatsapp_number = fields.Char(string='WhatsApp No.')
    social_network = fields.Char(string='Social Network ID')
    birth_place = fields.Char(string='Place of Birth')
    national_country_id = fields.Char(string='Country')
    nationality = fields.Char(string='Nationality')
    passport_no = fields.Char(string='Passport No.')
    national_id_no = fields.Char(string='National ID No.')
    passport_expire_date = fields.Date(string='Passport Expire Date')
    visa_no = fields.Char(string='Visa No.')
    visa_expire_date = fields.Date(string='Visa Expire Date')
    know_the_diu_from_website = fields.Boolean(string='From, DIU Website')
    know_the_diu_from_newspaper = fields.Boolean(string='Newspaper')
    know_the_diu_from_social_media = fields.Boolean(string='Social Media')
    know_the_diu_from_sms = fields.Boolean(string='SMS')
    know_the_diu_from_daffodil_family = fields.Boolean(string='Daffodil Family')
    know_the_diu_from_diu_student = fields.Boolean(string='DIU Student')
    know_the_diu_from_diu_employee = fields.Boolean(string='DIU Employee')
    know_the_diu_from_others = fields.Boolean(string='Others')

    is_parents_freedom_fighter = fields.Boolean(string='If your parent is Freedom Fighter')
    is_tribal = fields.Boolean(string='If you are a tribal')
    is_physical_disorder = fields.Boolean(string='If you are physically disorder')
    is_first_division_player = fields.Boolean(string='If you are a 1st division player')

    # Parents Details

    father_name = fields.Char(string='Father Name')
    father_contact_number = fields.Char(string='Mobile')
    father_email = fields.Char(string='Email')
    father_national_id = fields.Char(string='National ID')
    father_passport = fields.Char(string='Passport')
    father_birthday = fields.Date(string='Date of Birth')
    father_age = fields.Float(string='Age')
    father_occupation = fields.Char(string='Occupation')
    father_company = fields.Char(string='Company Name')
    father_designation = fields.Char(string='Designation')
    father_annual_income = fields.Float(string='Annual Income', default=0)
    father_annual_income_currency_symbol = fields.Selection([
        ('bdt', '৳'),
        ('dollar', '$'),
    ], string='Annual Income Currency Symbol', store=True)
    mother_name = fields.Char(string='Mother Name')
    mother_contact_number = fields.Char(string='Mobile')
    mother_email = fields.Char(string='Email')
    mother_national_id = fields.Char(string='National ID')
    mother_passport = fields.Char(string='Passport')
    mother_birthday = fields.Date(string='Date of Birth')
    mother_age = fields.Float(string='Age')
    mother_occupation = fields.Char(string='Occupation')
    mother_company = fields.Char(string='Company Name')
    mother_designation = fields.Char(string='Designation')
    mother_annual_income = fields.Float(string='Annual Income', default=0)
    mother_annual_income_currency_symbol = fields.Selection([
        ('bdt', '৳'),
        ('dollar', '$')], string='Annual Income Currency Symbol', store=True)

    # Local Guardian

    local_guardian_name = fields.Char(string='Name')
    local_guardian_relation = fields.Char(string='Relationship')
    local_guardian_contact_number = fields.Char(string='Mobile')
    local_guardian_email = fields.Char(string='Email')
    local_guardian_national_id = fields.Char(string='National ID')
    local_guardian_passport = fields.Char(string='Passport')
    local_guardian_street = fields.Char(string='Street', size=256)
    local_guardian_street2 = fields.Char(string='Street2', size=256)
    local_guardian_city = fields.Char(string='City', size=64)
    local_guardian_state_id = fields.Char(string='States')
    local_guardian_zip = fields.Char(string='Zip', size=8)
    local_guardian_country_id = fields.Char(string='Country')
    expanse_bearer = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('other', 'Others'),
    ], string='Expense Bearer', store=True)
    expanse_bearer_name = fields.Char(string='Name')
    expanse_bearer_relation = fields.Char(string='Relationship')
    expanse_bearer_contact_number = fields.Char(string='Mobile')
    expanse_bearer_national_id = fields.Char(string='National ID')
    expanse_bearer_passport = fields.Char(string='Passport')
    expanse_bearer_birthday = fields.Date(string='Date of Birth')
    expanse_bearer_age = fields.Float(string='Age')
    expanse_bearer_employer_name = fields.Char(string='Employer Name')
    expanse_bearer_occupation = fields.Char(string='Occupation')
    expanse_bearer_company = fields.Char(string='Company Name')
    expanse_bearer_designation = fields.Char(string='Designation')
    expanse_bearer_annual_income = fields.Float(string='Annual Income', default=0)
    expanse_bearer_annual_income_currency_symbol = fields.Selection([
        ('bdt', '৳'),
        ('dollar', '$'),
    ], string='Annual Income Currency Symbol', store=True)
    expanse_bearer_national_id_attachment = fields.Binary(string='Upload National ID', attachment=True, store=True,
                                                          help="Upload Applicant Expanse Bearer National ID.")
    expanse_bearer_signature_attachment = fields.Binary(string='Upload Signature', attachment=True, store=True,
                                                        help="Upload Applicant Expanse Bearer Signature.")
    expanse_bearer_street = fields.Char(string='Street', size=256)
    expanse_bearer_street2 = fields.Char(string='Street2', size=256)
    expanse_bearer_city = fields.Char(string='City', size=64)
    expanse_bearer_state_id = fields.Char(string='States')
    expanse_bearer_zip = fields.Char(string='Zip', size=8)
    expanse_bearer_country_id = fields.Char(string='Country')
    life_insurance = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('other', 'Others'),
    ], string='Life Insurance', store=True)
    life_insurance_name = fields.Char(string='Name')
    life_insurance_relation = fields.Char(string='Relationship')
    life_insurance_contact_number = fields.Char(string='Mobile')
    life_insurance_email = fields.Char(string='Email')
    life_insurance_national_id = fields.Char(string='National ID')
    life_insurance_passport = fields.Char(string='Passport')
    legal_guardian_name = fields.Char(string='Name')
    legal_guardian_date = fields.Date(string='Date', default=lambda self: fields.datetime.now())
    legal_guardian_signature_attachment = fields.Binary(string='Upload Signature', attachment=True, store=True,
                                                        help="Upload legal guardian Signature.")

    # Manual Documents

    is_manual_photographs = fields.Boolean(string='Manual Photographs')
    is_manual_ssc_certificate = fields.Boolean(string='SSC/Equivalent')
    is_manual_hsc_certificate = fields.Boolean(string='HSC/Equivalent')
    is_manual_bachelor_certificate = fields.Boolean(string='Bachelor')
    is_manual_ssc_transcript = fields.Boolean(string='SSC/Equivalent')
    is_manual_hsc_transcript = fields.Boolean(string='HSC/Equivalent')
    is_manual_bachelor_transcript = fields.Boolean(string='Bachelor')
    is_manual_photocopies_student = fields.Boolean(string='Student')
    is_manual_photocopies_guardian = fields.Boolean(string='Guardian')
    is_manual_copies_other_relevant_certificate = fields.Boolean(string='Manual copies of other relevant Certificates')
    is_manual_bring_main_certificates_transcripts = fields.Boolean(
        string='Manual bring Main Certificates and Transcripts')

    # Payment Details
    account_move_id = fields.Many2one(comodel_name="account.move", string="Invoice")
    invoice_amount_total_string = fields.Char(string="Total Amount")
    invoice_amount_residual_string = fields.Char(string="Amount Due")
    invoice_amount_paid_string = fields.Char(string="Amount Paid")
    invoice_payment_state = fields.Char(string="Payment Status")
    invoice_payment_date = fields.Date(string="Payment Date")
    invoice_payment_mediums = fields.Char(string='Payment Mediums')
    admission_fee_account_move_id = fields.Many2one(comodel_name="account.move", string="Invoice")
    admission_fee_invoice_amount_total_string = fields.Char(string="Total Amount")
    admission_fee_invoice_amount_residual_string = fields.Char(string="Amount Due")
    admission_fee_invoice_amount_paid_string = fields.Char(string="Amount Paid")
    admission_fee_invoice_payment_state = fields.Char(string="Payment Status")
    admission_fee_invoice_payment_state_allow_rel = fields.Char(string="Payment Status (Based on Allow Amount)")
    admission_fee_invoice_payment_mediums = fields.Text()
    admission_fee_invoice_payment_date = fields.Date(string="Payment Date")
    is_admission_fee_generated = fields.Boolean(string="Is Admission Fee Generated?", default=False, readonly=True)

    user_id = fields.Many2one(comodel_name='res.users', string='User')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name_concat(self):
        for partner in self:
            if not partner.middle_name:
                partner.name = str(partner.first_name) + " " + str(
                    partner.last_name
                )
            else:
                partner.name = str(partner.first_name) + " " + str(
                    partner.middle_name) + " " + str(partner.last_name)

    def submit_form(self):
        self.state = 'submit'

    def admission_confirm(self):
        self.state = 'admission'

    def confirm_in_progress(self):
        for record in self:
            record.state = 'confirm'

    def confirm_rejected(self):
        self.state = 'reject'

    def confirm_pending(self):
        self.state = 'pending'

    def confirm_to_draft(self):
        self.state = 'draft'

    def confirm_cancel(self):
        self.state = 'cancel'
        if self.is_student and self.student_id.fees_detail_ids:
            self.student_id.fees_detail_ids.state = 'cancel'

    def update_user_password_admission_applicant_student(self):
        for record in self:
            if record.student_id and record.mobile:
                if record.student_id.user_id:
                    record.student_id.user_id.write({'password': record.mobile})

    # enroll student
    def enroll_student(self):
        for record in self:
            record.admission_date = datetime.date.today().strftime('%Y-%m-%d')
            # super(SeApplicant, self).enroll_student()

            # ## Create invoice for Admission Fee
            # self.create_invoice_admission_applicant_admission_fee()

            ## Update Student login Password using Mobile number
            self.update_user_password_admission_applicant_student()

            ## Update Partner
            if record.partner_id:
                record.partner_id.sudo().write({
                    'email': self.email,
                    'is_admission_applicant': True,
                    'is_student': True,
                })

            if record.student_id:
                student = self.env['se.student'].browse(record.student_id.id)
                if student:
                    student.write({
                        'emergency_contact_info': record.emergency_contact_info,
                        'student_type_id': record.student_type_id.id,
                        'education_shift_id': record.education_shift_id.id,
                        'batch_id': record.batch_id.id,
                        # 'curriculum_id': record.curriculum_id.id,
                        # 'syllabus_id': record.curriculum_id.syllabus_id.id,
                        # 'payment_scheme_id': record.curriculum_id.payment_scheme_id.id,
                        # 'semester_id': record.register_id.semester_id.id,
                        # 'semester_year': record.register_id.semester_year,
                        # 'semester_year_string': record.register_id.semester_year_string,
                        # 'semester_type': record.semester_type_id.id,
                    })
        record.state = 'done'

    # def get_educational_board_result(self, exam_name, educational_board, roll_number, year):
    #     try:
    #         url = "http://ebapi.teletalk.com.bd/v1.0/ebapi.php"
    #         headers = {
    #             "Content-Type": "application/json",
    #             "APIKEY": "d49c6512c7134fe5c0ce5595873bb7a4",
    #         }
    #         data = {
    #             "commandID": "getDetailsResult",
    #             "exam": exam_name,
    #             "board": educational_board,
    #             "rollNo": roll_number,
    #             "year": year
    #         }
    #         response = requests.get(url=url, headers=headers, data=json.dumps(data))
    #         if response.status_code == 200 or response.status_code == 201:
    #             data = response.json()
    #             return data
    #     except:
    #         pass

    # Get SSC and HSC Result
    def get_educational_board_result_ssc_and_hsc(self):
        error_message = ""
        error_message_status = False
        application = self.env['se.applicant'].browse(self.id)
        if application:
            error_message = "Some of the required fields for Education Board result is empty. Ex."
            if not application.education_board_ssc_id:
                error_message = error_message + "\nEducation Board of SSC"
                error_message_status = True
            else:
                if not application.education_board_ssc_id.education_board_code:
                    error_message = error_message + "\nEducation Board Code is not setted for: " + str(
                        application.education_board_ssc_id.name)
                    error_message_status = True

            if not application.roll_number_ssc:
                error_message = error_message + "\nRoll Number of SSC"
                error_message_status = True

            if not application.year_ssc:
                error_message = error_message + "\nYear of SSC"
                error_message_status = True

            if not application.education_board_hsc_id:
                error_message = error_message + "\nEducation Board of HSC"
                error_message_status = True
            else:
                if not application.education_board_ssc_id.education_board_code:
                    error_message = error_message + "\nEducation Board Code is not setted for: " + str(
                        application.education_board_ssc_id.name)
                    error_message_status = True

            if not application.roll_number_hsc:
                error_message = error_message + "\nRoll Number of HSC"
                error_message_status = True

            if not application.year_hsc:
                error_message = error_message + "\nYear of HSC"
                error_message_status = True

            if error_message_status:
                raise UserError(error_message)

            ## Get SSC Result
            exam_name = "ssc"
            educational_board = application.education_board_ssc_id.education_board_code
            roll_number = application.roll_number_ssc
            year = application.year_ssc
            result = self.get_educational_board_result(exam_name, educational_board, roll_number, year)

            ## Insert Records of SSC Result
            self.env["se.applicant.board.result.general"].search(
                [('exam_name_ref', '=', 'ssc'), ('applicant_id', '=', self.id)]).unlink()
            if result:
                for item in result['subject']:
                    self.env["se.applicant.board.result.general"].sudo().create({
                        'subject_name': str(item['subName']),
                        'subject_code': str(item['subCode']),
                        'grade': str(item['grade']),

                        'exam_name_ref': str(exam_name.lower()),
                        'educational_board': str(educational_board.lower()),
                        'roll_number': str(result['rollNo']),
                        'registration_number': str(result['regNo']),
                        'passing_year': str(result['passYear']),

                        'applicant_id': int(self.id),
                    })
                self.sudo().write({
                    'roll_number_ssc': str(result['rollNo']),
                    'registration_number_ssc': str(result['regNo']),
                    'ssc_grade': str(result['result']),
                    'ssc_gpa': str(result['gpa']),
                    'is_get_educational_board_result_ssc': True
                })

            ## Get HSC Result
            exam_name = "hsc"
            educational_board = application.education_board_hsc_id.education_board_code
            roll_number = application.roll_number_hsc
            year = application.year_hsc
            result = self.get_educational_board_result(exam_name, educational_board, roll_number, year)

            ## Insert Records of HSC Result
            self.env["se.applicant.board.result.general"].search(
                [('exam_name_ref', '=', 'hsc'), ('applicant_id', '=', self.id)]).unlink()
            if result:
                for item in result['subject']:
                    self.env["se.applicant.board.result.general"].sudo().create({
                        'subject_name': str(item['subName']),
                        'subject_code': str(item['subCode']),
                        'grade': str(item['grade']),

                        'exam_name_ref': str(exam_name.lower()),
                        'educational_board': str(educational_board.lower()),
                        'roll_number': str(result['rollNo']),
                        'registration_number': str(result['regNo']),
                        'passing_year': str(result['passYear']),

                        'applicant_id': int(self.id),
                    })
                self.sudo().write({
                    'roll_number_hsc': str(result['rollNo']),
                    'registration_number_hsc': str(result['regNo']),
                    'hsc_grade': str(result['result']),
                    'hsc_gpa': str(result['gpa']),
                    'is_get_educational_board_result_hsc': True
                })

    # Create Invoice
    def create_invoice_admission_applicant_admission_fee(self):
        for record in self:
            if not record.register_id.admission_fee_id:
                raise UserError("Admission Fee is not settled.")

            if not record.student_id.student_id:
                raise UserError("Student ID is not assigned.")

            if not record.admission_fee_account_move_id:
                account_move = self.env['account.move'].sudo().create({
                    'name': "INV/" + str(datetime.now().year) + "/" + str(
                        record.application_number) + "/STU" + str(record.student_id.student_id),
                    'partner_id': record.student_id.partner_id.id,
                    'ref': str(record.id),
                    'is_admission_applicant_invoice': True,
                    'applicant_id': record.id,
                    'student_id': record.student_id.id,
                    'type': 'out_invoice',
                    'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': record.register_id.admission_fee_id.id,
                        'name': record.register_id.admission_fee_id.name,
                        'account_id': False,
                        'price_unit': record.register_id.admission_fee_id.list_price,
                        'quantity': 1.0,
                        'discount': 0.0,
                        'product_uom_id': record.register_id.admission_fee_id.uom_id.id,
                    })],
                })
                if account_move:
                    invoice_post_status = account_move.sudo().action_post()
                    record.sudo().write({
                        'admission_fee_account_move_id': account_move.id,
                        'is_admission_fee_generated': True,
                    })

