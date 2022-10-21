from odoo import api, models, fields, _
import math


class LimsInspection(models.Model):
    _name = 'lims.inspection'
    _description = 'Inspection'
    _inherit = ['mail.thread', 'mail.activity.mixin']

# TODO: adicionar no índice do record para todos os records do lims
    ref = fields.Char(string = 'Inspection Number')
    name = 'New Inspection'
    
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)

    lot_id = fields.Many2one(
        'stock.production.lot',
        string='Lot/Serial',
        required=True,
        domain="[('product_id', '=', product_id)]")

    lot_size = fields.Float(related='lot_id.product_qty')
    
    date_created = fields.Date(
        string='Creation Date', default=fields.Datetime.now())
    
    date_approved = fields.Date(string='Approval Date')
    
    responsible_uid = fields.Many2one('res.users', string='Responsible')
    
    approver_uid = fields.Many2one('res.users', string='Approver')

    sample_size = fields.Float(string = 'Sample Size', compute='_calculate_sample_size')
    sampling_date = fields.Datetime(string = "Sampling Date")
    

    status = fields.Selection(
        [('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('pass', 'Passed'),
        ('fail', 'Failed'),
        ('cancel', 'Cancelled')],
        default='open', required = True, tracking = True
    )

    lost_qty = fields.Float(
        'Quantity consumed',
        help = 'This field indicates how much of the product was used to conduct the required tests.'
        )

    analysis_ids = fields.One2many(
        comodel_name= 'lims.analysis',
        inverse_name = 'inspection_id'
        )


    def action_validate(self):
        for rec in self:
            rec.status = "pass"

    def action_cancel_inspection(self):
        for rec in self:
            rec.status = "cancel"

    @api.depends('sample_size')
    def _calculate_sample_size(self):
        for rec in self:
            lot_size = rec.lot_size
            if rec.lot_size:
                rec.sample_size = 1 + math.ceil(math.sqrt(lot_size))
            else:
                rec.sample_size = 0
        return rec.sample_size

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('lims.inspection')
        return super(LimsInspection, self).create(vals)

# TODO: Create a method to get specification from products
# https://www.youtube.com/watch?v=BSL4iOHZ-Rc
# Standardize o2m field names

    # @api.model
    # def default_get(self, fields):
    #     res = super(LimsInspection, self).default_get(fields)
    #     analysis_ids = [(5,0,0)]
    #     specification_rec = self.env['lims.specification'].search([])
    #     for spec in specification_rec:
    #         line = (0, 0, {
    #             'specification_id': spec.id,
    #             'value_range': spec.value_range
    #         },)
    #         analysis_ids.append(line)
    #     res.update({
    #         'analysis_ids': analysis_ids
    #     })
    #     return res
