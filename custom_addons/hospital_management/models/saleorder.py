from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    appointment_id = fields.Many2one(
        "hospital.appointment",
        string="Appointment"
    )

    consultation_id = fields.Many2one(
        "hospital.consultation",
        string="Consultation")