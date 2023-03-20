# -*- coding: utf-8 -*-
# from odoo import http


# class SeAdmission(http.Controller):
#     @http.route('/se_applicant/se_applicant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/se_applicant/se_applicant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('se_applicant.listing', {
#             'root': '/se_applicant/se_applicant',
#             'objects': http.request.env['se_applicant.se_applicant'].search([]),
#         })

#     @http.route('/se_applicant/se_applicant/objects/<model("se_applicant.se_applicant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('se_applicant.object', {
#             'object': obj
#         })
