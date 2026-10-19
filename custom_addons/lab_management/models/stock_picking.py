from odoo import api,models,fields
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    payment_status = fields.Selection([
        ('paid','Paid'),
        ('not_paid','Not Paid'),],
        string="Payment Status",)

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code == 'outgoing':
                if not picking.payment_status:
                    raise ValidationError(
                        "Choose Payment Status."
                    )
                elif picking.payment_status != 'paid':
                    raise ValidationError(
                        "You cannot validate this delivery because the payment has not been completed."
                    )

        return super().button_validate()