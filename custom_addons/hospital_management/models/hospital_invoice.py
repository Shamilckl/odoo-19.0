from odoo import models, fields

class HospitalInvoice(models.Model):
    _inherit = "account.move.line"

    dosage = fields.Float(string="Dosage")