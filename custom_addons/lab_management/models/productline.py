from odoo import api, fields, models


class ProductLine(models.TransientModel):
    _name = 'product.line'
    _description = 'Product Line'

    name = fields.Char(
        string="Product Sequence",
        readonly=True,
        copy=False,
    )

    product_relation = fields.Many2one(
        'product.wizard',
        string="Relation"
    )

    product_name = fields.Many2one(
        'product.template',
        string="Product Name"
    )

    quantity = fields.Float(
        string="Quantity"
    )

    price = fields.Float(
        string="Price",
        related="product_name.list_price"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'product.line'
                )

        return super().create(vals_list)