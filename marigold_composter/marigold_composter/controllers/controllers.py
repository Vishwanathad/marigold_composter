# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class WebsiteSnippet(http.Controller):
    @http.route('/total_waste_count', auth="public", type="json")
    def total_waste(self, **kw):
      
      # get total waste data from database
      query = """SELECT 
            SUM(s.waste) AS collected_waste, 
            SUM(s.cocopeat) AS proceesed_cocopeat, 
            SUM(s.compost) AS proceesed_compost, 
            SUM(s.sieved_compost) AS sieved_compost
          from 
            sale_order as s  """
      request.env.cr.execute(query)
      (collected_waste,proceesed_cocopeat,proceesed_compost,sieved_compost) = request.env.cr.fetchall()[0]
      
      # get total no of homes
      query = """SELECT SUM(no_homes) AS no_homes from res_partner where type = 'other';  """
      request.env.cr.execute(query)
      no_of_homes = request.env.cr.fetchall()[0][0]
      return   {
        "collected_waste" : collected_waste,
        "proceesed_cocopeat" : proceesed_cocopeat,
        "proceesed_compost" : proceesed_compost,
        "sieved_compost" : sieved_compost,
        "no_of_homes": no_of_homes
      }
      
      

        

# class MyModule(http.Controller):
#     @http.route('/my_module/my_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_module/my_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_module.listing', {
#             'root': '/my_module/my_module',
#             'objects': http.request.env['my_module.my_module'].search([]),
#         })

#     @http.route('/my_module/my_module/objects/<model("my_module.my_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_module.object', {
#             'object': obj
#         })