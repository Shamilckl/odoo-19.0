from odoo import models, fields

class Hospitallaboratory(models.Model):
    _name = "hospital.laboratory"
    _description = "Hospital Laboratory"
    _rec_name = "name"

    name = fields.Many2one("hospital.patient", string="Patient")

    test = fields.Char(string="Name of Test")

    amount = fields.Float(string="Amount")

