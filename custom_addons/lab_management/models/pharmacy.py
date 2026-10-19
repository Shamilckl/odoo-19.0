from odoo import fields, models, api

class LabPharmacy(models.Model):
    _name = 'lab.pharmacy'
    _description = 'Lab Pharmacy'

    patient_name = fields.Many2one("lab.patient", string='Patient Name', readonly=True)
    doctor_name = fields.Many2one("lab.doctor",string='Doctor Name', readonly=True)
    consultation_date = fields.Date('Date',readonly=True)
    product_line_ids=fields.One2many('pharmacy.line','pharmacy_relation',string='Product')

    price_total = fields.Float(
        string='Total',
        compute='_compute_amount'
    )

    @api.depends('product_line_ids.subtotal')
    def _compute_amount(self):
        for appointment in self:
            appointment.price_total = sum(
                appointment.product_line_ids.mapped('subtotal')
            )