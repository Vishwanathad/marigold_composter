# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,time


class Partner(models.Model):
    _inherit = 'res.partner'
    
    no_homes = fields.Integer(string="No of Homes")

    