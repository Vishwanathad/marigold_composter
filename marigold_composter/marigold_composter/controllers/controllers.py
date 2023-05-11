# -*- coding: utf-8 -*-
from decimal import Decimal
import odoo
from odoo import http
from odoo.http import request
import math
from odoo.addons.website.controllers.main import Website


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
      if proceesed_cocopeat is None:
          proceesed_cocopeat = 0
      else:
          proceesed_cocopeat = math.ceil(proceesed_cocopeat/1000)
      if proceesed_compost is None:
          proceesed_compost = 0
      else:
          proceesed_compost = math.ceil(proceesed_compost/1000)
      if sieved_compost is None:
          sieved_compost = 0
      else:
          sieved_compost = math.ceil(sieved_compost/1000)
      if collected_waste is None:
          collected_waste = 0
      else:
          collected_waste = math.ceil(collected_waste/1000)
      if no_of_homes is None:
          no_of_homes = 0
      else:
          no_of_homes = f'{Decimal(str(no_of_homes)):n}'
          
      return   {
        "collected_waste" : collected_waste,
        "proceesed_cocopeat" : proceesed_cocopeat,
        "proceesed_compost" : proceesed_compost,
        "sieved_compost" : sieved_compost,
        "no_of_homes": no_of_homes
      }
      
class MarigoldRedirectAfterLoginController(Website):

    # ------------------------------------------------------
    # Login - overwrite of the web login so that regular users are redirected to the backend
    # while portal users are redirected to the frontend by default
    # ------------------------------------------------------

    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                module_name, menu_xml_id = "marigold_composter", "sale_menu_root"
                menu_id = request.env.ref('sale.sale_menu_root')
                redirect = '/web#menu_id='+str(menu_id.id)
            else:
                redirect = '/ln/dashboard'
            return request.redirect(redirect)
        return response
      
      

        

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