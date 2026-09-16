from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dosage = fields.Float(
        string="Dosage"
    )

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)
        values["dosage"] = self.dosage
        return   values
