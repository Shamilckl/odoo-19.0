from odoo import api,fields, models

class ProductWizard(models.TransientModel):
    _name = 'product.wizard'
    _description = 'Product Wizard'

    products = fields.Many2one('product.template', string='Products')

    product_category = fields.Selection([
        ('return_product', 'Return'),
        ('replacement', 'Replacement'),
        ('add_new_product', 'Add New Product'),
        ('reship_product', 'Reship Product'),
        ('extra_customer_charges', 'Extra Customer Charges')],
        string='Product Category',)

    reason = fields.Many2one("written.reasons",string='Reason')

    product_line_ids = fields.One2many('product.line','product_relation',string='Products')