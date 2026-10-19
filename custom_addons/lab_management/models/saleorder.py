from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    vip_boolean=fields.Boolean(string="VIP Customer",default=False,compute='_compute_vip_boolean')

    def action_open_appointment_wizard(self):
        # pass
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Product',
            'res_model': 'product.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    @api.depends('amount_total')
    def _compute_vip_boolean(self):
        for order in self:
            if order.amount_total>1000:
                order.vip_boolean = True
            else:
                self.vip_boolean = False