# -*- coding: utf-8 -*-
from odoo import models, fields, _

class LimsCriteria(models.Model):
    _name = "lims.criteria" 
    _inherit = ['mail.thread', 'mail.activity.mixin'] # herdar campos destes modelos
    _description = "Criteria"
    
    name = fields.Char(string = "Analysis Criteria", required = True)
    description = fields.Html(string = "Description")
    method = fields.Char(string="Method", tracking=True, required = True)
    uom_id = fields.Many2one('uom.uom', string = 'Unit of Measure')
    type = fields.Selection([
        ('numeric','Numeric'),
        ('quali','Qualitative')
        ], string = "Type of Criteria", required = True)
    equipment_id = fields.Many2one('maintenance.equipment')
