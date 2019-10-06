# -*- coding: utf-8 -*-
from openerp import http

# class HrModRealEstate(http.Controller):
#     @http.route('/hr_mod_real_estate/hr_mod_real_estate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_mod_real_estate/hr_mod_real_estate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_mod_real_estate.listing', {
#             'root': '/hr_mod_real_estate/hr_mod_real_estate',
#             'objects': http.request.env['hr_mod_real_estate.hr_mod_real_estate'].search([]),
#         })

#     @http.route('/hr_mod_real_estate/hr_mod_real_estate/objects/<model("hr_mod_real_estate.hr_mod_real_estate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_mod_real_estate.object', {
#             'object': obj
#         })