from odoo import api, fields, models

class Order(models.Model):
    _inherit = 'sale.order'
    
    start_time = fields.Float(string='Start Time')
    end_time = fields.Float(string='End Time')
    waste = fields.Integer(string= 'Waste (kgs)')
    staff = fields.Integer(string='Staff')
    cocopeat = fields.Integer(string='Cocopeat used(kgs)')
    compost = fields.Integer(string="Compost used(kgs)")
    Sieved_compost = fields.Integer(string="Sieved Compost (kgs)")
    remarks = fields.Char(string="Remarks")
    temp_360_lit_1 = fields.Integer(string="Temperature 360 Lit 1")
    temp_360_lit_2 = fields.Integer(string="Temperature 360 Lit 2")
    temp_360_lit_3 = fields.Integer(string="Temperature 360 Lit 3")