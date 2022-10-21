from odoo import api, models, fields, _

class LimsProductSpecification(models.Model):
    _name = 'product.product'
    _description = 'Product Specifications'
    _inherit = 'product.product'

    
    specification_ids = fields.One2many(
        'lims.specification',
        'product_id',
        string = 'Specification')



class LimsSpecification(models.Model):
    _name = 'lims.specification'
    _description = 'Product Specification'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string = "Specification Name")
    ref = fields.Char(string = "Specification Number")
    
    product_id = fields.Many2one('product.product', string = 'Product')
    
    criteria_id = fields.Many2one('lims.criteria', required = True)
    condition = fields.Char(string = 'Analysis Condition')
    type = fields.Selection(related = 'criteria_id.type', required = True, default = 'numeric')
    
    reference_value = fields.Float(
        string= 'Reference', 
        digits=(12,6), 
        tracking = True)
    
    tolerance_value = fields.Float(
        string= 'Tolerance', 
        digits=(12,6), 
        default = 0, 
        tracking = True)

    uom_id = fields.Many2one(string = "UoM", related = 'criteria_id.uom_id')

    operator = fields.Selection([
        ('characteristic','Characteristic'),
        ('lt','<'),
        ('gt','>'),
        ('le','<='),
        ('ge','>='),
        ('equal',' = ')
    ],
    default = 'equal',
    string = 'Mode')

    value_range = fields.Char(
        string = 'Acceptance Value',
        compute = '_compute_value_range',
        inverse = '_set_value_range',
        store = True,
        tracking = True)


    @api.depends('operator')
    def _set_value_range(self):
        self.ensure_one()
        for rec in self:
            if rec.operator == 'characteristic':
                continue

    @api.depends('reference_value', 'tolerance_value', 'operator')
    def _compute_value_range(self):
        self.ensure_one()
        for rec in self:
            range_min = self.reference_value - self.tolerance_value
            range_max = self.reference_value + self.tolerance_value
            if rec.reference_value:
                if rec.operator == 'equal':
                    range = (str(range_min), str(range_max))
                    rec.value_range = " - ".join(range)
                if rec.operator == 'lt':
                    range = (str(range_max))
                    rec.value_range = "< " + range
                if rec.operator == 'le':
                    range = (str(range_max))
                    rec.value_range = "<= " + range
                if rec.operator == 'gt':
                    range = (str(range_min))
                    rec.value_range = "> " + range
                if rec.operator == 'ge':
                    range = (str(range_min))
                    rec.value_range = ">= " + range
            else:
                rec.value_range = ""
        return rec.value_range
