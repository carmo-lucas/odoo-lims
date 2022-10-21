from odoo import models, fields, _, api

class LimsAnalysis(models.Model):
    _name = 'lims.analysis'
    _description = 'Inspection Analysis'
    
    ref = fields.Char(string='Analysis ID')
    criteria_id = fields.Many2one('lims.criteria')
    inspection_id = fields.Many2one('lims.inspection', string = 'Inspection')
    specification_id = fields.Many2one('lims.specification')
    specification_acceptance = fields.Char(related = 'specification_id.value_range')
    date_input = fields.Datetime(string = 'Date Input')


    numeric_result = fields.Float(string = 'Numerical Result')
    qualitative_result = fields.Boolean(string = 'Pass/Fail')
    qualitative_result_description = fields.Char(string = 'Description')
    
    responsible_uid = fields.Many2one('res.users', string='Responsible')

    analysis_status = fields.Selection([
        ('open','Open'),
        ('conform','Conform'),
        ('non_conform','Nonconform'),
        ('undefined','Undefined'),
    ], string = 'Analysis Status', required=True, default = 'open')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('lims.analysis')
        return super(LimsAnalysis, self).create(vals)