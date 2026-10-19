from odoo import fields, models, api


class PharmacyLine(models.Model):
    _name = 'pharmacy.line'
    _description = 'Pharmacy Line'

    pharmacy_relation = fields.Many2one(
        'lab.pharmacy',
        string='Pharmacy'
    )

    product_name = fields.Many2one(
        'product.template',
        string='Product',
        readonly=True
    )

    comment = fields.Char(
        string='Comment',
        readonly=True
    )

    days = fields.Integer(
        string='Days',
        readonly=True
    )

    quantity = fields.Integer(
        string='Quantity',
        readonly=True
    )

    unit_price = fields.Float(
        string='Price',
        readonly=True
    )

    subtotal = fields.Float(
        string='Subtotal',
        readonly=True
    )

    price_total = fields.Float(
        string="Total",
        compute='_compute_amount')

    @api.depends('subtotal')
    def _compute_amount(self):
        for line in self:
            line.price_total = line.subtotal