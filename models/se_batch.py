from odoo import api, fields, models


class SeBatch(models.Model):
    _inherit = 'se.batch'

    _description = 'SmartEdu Batch'

    name = fields.Char(string='Name', required=False)
    code = fields.Char(string='Name', required=False)
    note = fields.Char(string='Name', required=False)
    active = fields.Char(string='Name', required=False)

    semester_id = fields.Many2one(comodel_name='se.semester', string='Semester', domain=[('is_active', '=', True)])
    semester_year = fields.Date(string='Year')
    semester_year_string = fields.Char(string='Year')
    # semester_type_id = fields.Many2one(comodel_name='se.semester.type', string='Semester Type',
    #                                    related="semester_id.semester_type_id")

    number = fields.Integer(string='Batch No.')
    # curriculum_id = fields.Many2one(comodel_name='se.academic.curriculum', string='Curriculum',
    #                                 domain=[('active', '=', True)])
    # syllabus_id = fields.Many2one(comodel_name='op.academic.syllabus', string='Syllabus',
    #                               domain=[('active', '=', True)])
    # payment_scheme_id = fields.Many2one(comodel_name='op.academic.payment.scheme', string='Payment Scheme',
    #                                     domain=[('active', '=', True)])

    def _get_years(self):
        year_list = []

        ## Static Year Range
        # current_year = int(datetime.now().year)
        # for i in range(current_year - 10, current_year + 11):
        #     year_list.append((str(i), str(i)))

        ## Configuration Year Range
        openeducat_semester_year_range_start = self.env['ir.config_parameter'].sudo().get_param(
            'openeducat_semester.year_range_start')
        openeducat_semester_year_range_end = self.env['ir.config_parameter'].sudo().get_param(
            'openeducat_semester.year_range_end')
        for i in range(int(openeducat_semester_year_range_start), int(openeducat_semester_year_range_end) + 1):
            year_list.append((str(i), str(i)))

        return year_list

    @api.model
    def create(self, vals):
        if 'semester_year' in vals.keys():
            semester_year = parser.parse(str(vals["semester_year"]))
            vals["semester_year_string"] = semester_year.year
        vals['code'] = self.env['ir.sequence'].next_by_code('op.batch')
        res = super(OpBatch, self).create(vals)
        return res

    def write(self, vals):
        if 'semester_year' in vals.keys():
            semester_year = parser.parse(str(vals["semester_year"]))
            vals["semester_year_string"] = semester_year.year
        res = super(OpBatch, self).write(vals)
        return res

    @api.onchange('curriculum_id')
    def onchange_curriculum_id(self):
        for rec in self:
            rec.syllabus_id = rec.curriculum_id.syllabus_id
            rec.payment_scheme_id = rec.curriculum_id.payment_scheme_id