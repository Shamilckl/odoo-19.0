from odoo import models, fields

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
        domain="[('product_tmpl_id.is_medicine','=',True)]"
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

