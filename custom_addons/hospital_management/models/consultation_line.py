from odoo import models, fields, api

class ConsultationLine(models.Model):
    _name = "hospital.consultation.line"
    _description = "Consultation Medicine"
    _rec_name = "medicine_id"

    consultation_id = fields.Many2one(
        "hospital.consultation",
        string="Consultation"
    )

    medicine_id = fields.Many2one(
        "product.product",
        string="Medicine",
        domain="[('product_tmpl_id.is_medicine', '=', True)]"
    )

    dosage = fields.Float(string="Dosage in mg")

    quantity = fields.Integer(
        string="Quantity",
        default=1
    )

    price = fields.Float(
        related="medicine_id.lst_price",
        string="Price"
    )

    @api.model_create_multi
    def create(self, vals_list):

        lines = super().create(vals_list)

        for line in lines:

            if not line.consultation_id:
                continue

            sale_order = self.env["sale.order"].search([
                ("consultation_id", "=", line.consultation_id.id)
            ], limit=1)

            if sale_order:
                self.env["sale.order.line"].create({
                    "order_id": sale_order.id,
                    "product_id": line.medicine_id.id,
                    "product_uom_qty": line.quantity,
                    "price_unit": line.medicine_id.lst_price,
                })

        return lines