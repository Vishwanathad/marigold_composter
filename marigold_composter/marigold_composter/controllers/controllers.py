# -*- coding: utf-8 -*-
from decimal import Decimal
import odoo
from odoo import http
from odoo.http import request
import math
import calendar
from odoo.addons.website.controllers.main import Website

def query_total_waste():
    query = """SELECT 
            SUM(s.waste) AS collected_waste, 
            SUM(s.cocopeat) AS proceesed_cocopeat, 
            SUM(s.compost) AS proceesed_compost, 
            SUM(s.sieved_compost) AS sieved_compost
          from 
            sale_order as s  """
    request.env.cr.execute(query)
    (collected_waste, proceesed_cocopeat, proceesed_compost,
     sieved_compost) = request.env.cr.fetchall()[0]

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

    return {
        "collected_waste": collected_waste,
        "proceesed_cocopeat": proceesed_cocopeat,
        "proceesed_compost": proceesed_compost,
        "sieved_compost": sieved_compost,
        "no_of_homes": no_of_homes
    }


class WebsiteSnippet(http.Controller):
    @http.route('/total_waste_count', auth="public", type="json")
    def total_waste(self, **kw):

        # get total waste data from database
        waste_count = query_total_waste()
        return waste_count


class MarigoldRedirectAfterLoginController(Website):

    # ------------------------------------------------------
    # Login - overwrite of the web login so that regular users are redirected to the backend
    # while portal users are redirected to the frontend by default
    # ------------------------------------------------------

    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(
            redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                # module_name, menu_xml_id = "marigold_composter", "sale_menu_root"
                # menu_id = request.env.ref('sale.sale_menu_root')
                # redirect = '/web#menu_id='+str(menu_id.id)
                redirect = '/mc/dashboard'
            else:
                redirect = '/mc/dashboard'
            return request.redirect(redirect)
        return response


class MarigoldDashboard(http.Controller):
    @http.route('/mc/dashboard', auth='user', type='http', website=True)
    def get_dashboard(self, **kw):
        # get total waste data from database to dashboard
        table_result = []
        template = 'marigold_composter.marigold_dashboard'
        waste_total = query_total_waste()
        query_table = """SELECT subquery1.name,
                    subquery1.collected_waste,
                    subquery2.homes
                    FROM   (SELECT res_partner.name,
                    Sum(sale_order.waste) AS collected_waste
                    FROM   res_partner
                    INNER JOIN sale_order
                    ON res_partner.id = sale_order.partner_invoice_id
                    WHERE  Extract(month FROM date_order) = Extract(
                    month FROM CURRENT_DATE)
                    AND Extract(year FROM date_order) = Extract(
                    year FROM CURRENT_DATE)
                    GROUP  BY res_partner.name) AS subquery1
                    INNER JOIN (SELECT t1.name,
                    Sum(t2.no_homes) AS homes
                    FROM   res_partner t1
                    JOIN res_partner t2
                    ON t1.id = t2.parent_id
                    GROUP  BY t1.name) AS subquery2
                    ON subquery1.name = subquery2.name
                    WHERE  subquery1.collected_waste IS NOT NULL
                    AND subquery2.homes IS NOT NULL
                    ORDER BY subquery1.collected_waste  desc limit 5; """ 
        request.env.cr.execute(query_table)
        table_data = request.env.cr.fetchall() 
        for item in table_data:
            table_result.append({
                "company_name" : item[0],
                "waste_in_tons" : (item[1]/1000),
                "homes" : item[2]
            })
        card_view = request.render(template, {
            "collected_waste": waste_total['collected_waste'],
            "proceesed_cocopeat": waste_total['proceesed_cocopeat'],
            "proceesed_compost": waste_total['proceesed_compost'],
            "sieved_compost": waste_total['sieved_compost'],
            "no_of_homes": waste_total['no_of_homes'],
            "table_result":table_result
        })

        return card_view

    @http.route('/mc/barchart/chartdata', auth='user', type='json')
    def get_waste_collected(self, **kw):
        result_list ={}
        formTwoData = {}
        
        labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        query = """SELECT
                EXTRACT(month FROM date_order) AS month,
                SUM(waste) AS collected_waste
                FROM sale_order
                WHERE EXTRACT(year FROM date_order) = EXTRACT(year from current_date)
                GROUP BY EXTRACT(month FROM date_order)"""
        request.env.cr.execute(query)
        bar_data = request.env.cr.fetchall()
        waste_collected = {}
        for item in bar_data:
            waste_collected[calendar.month_abbr[int(item[0])]] = item[1]/1000
            
            
        query_multi_bar = """WITH monthly_performance AS (
                SELECT EXTRACT(month FROM date_order) AS month, res_partner.name as  performer_name,  sum(sale_order.waste) as wastes
                FROM res_partner
	            INNER JOIN sale_order ON res_partner.id=sale_order.partner_invoice_id 
                WHERE EXTRACT(year FROM date_order) = EXTRACT(year from current_date)  and sale_order.waste IS NOT NULL
                GROUP BY res_partner.name, month
                ),
                ranked_performance AS (
                SELECT performer_name, month, wastes,  ROW_NUMBER() OVER (PARTITION BY month ORDER BY wastes DESC) AS rank
                FROM monthly_performance
                )
                SELECT month, performer_name, wastes
                FROM ranked_performance
                WHERE rank <=5
                ORDER BY month, wastes desc;"""
        request.env.cr.execute(query_multi_bar)
        query_data = request.env.cr.fetchall() 
        
        
        for item in query_data:
            key = calendar.month_abbr[int(item[0])]
            value = item[1:]
            
            if key in result_list:
                result_list[key].append(value)
            else:
                result_list[key]=[value]     
        for index,item in enumerate(labels):
            if item in result_list:
                for array_item in result_list[item]:
                    if array_item[0] not in formTwoData:
                        formTwoData[array_item[0]] = [0 for i in range(12)]
                    formTwoData[array_item[0]].insert(index,array_item[1]/1000 if array_item[1] is not None else 0 ) 
                    
          

        return {"waste_collected":waste_collected,
                "formTwoData":formTwoData}