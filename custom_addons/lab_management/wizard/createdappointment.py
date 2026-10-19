from odoo import api, fields, models


class CreatedAppointment(models.TransientModel):
    _name = 'created.appointment'
    _description = 'Created Appointment'

    patient_name = fields.Many2one("lab.patient", string='Patient Name', readonly=True)
    doctor_name = fields.Many2one("lab.doctor", string='Doctor Name', readonly=True)
    consultation_date = fields.Date('Date', readonly=True)
    age = fields.Float('Age')

    product_line_ids = fields.One2many('appointment.line', 'appointment_relation', string='Product')

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

    def action_confirm_prescription(self):
        self.ensure_one()

        pharmacy = self.env['lab.pharmacy'].create({
            'patient_name': self.patient_name.id,
            'doctor_name': self.doctor_name.id,
            'consultation_date': self.consultation_date,
        })

        for line in self.product_line_ids:
            self.env['pharmacy.line'].create({
                'pharmacy_relation': pharmacy.id,
                'product_name': line.product_name.id,
                'comment': line.comment,
                'days': line.days,
                'quantity': line.quantity,
                'unit_price': line.unit_price,
                'subtotal': line.subtotal,
                'price_total': line.price_total,
            })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Pharmacy',
            'res_model': 'lab.pharmacy',
            'view_mode': 'form',
            'res_id': pharmacy.id,
            'target': 'current',
        }
