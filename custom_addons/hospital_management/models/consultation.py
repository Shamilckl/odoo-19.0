from odoo import models, fields, api

class HospitalConsultation(models.Model):
    _name = "hospital.consultation"
    _description = "Consultation"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Consultation No",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )

    appointment_id = fields.Many2one(
        "hospital.appointment", tracking=True
    )

    patient_id = fields.Many2one(
        "hospital.patient", tracking=True
    )

    doctor_id = fields.Many2one(
        "hospital.doctor", tracking=True
    )

    diagnosis = fields.Text()

    medicine_line_ids = fields.One2many(
        "hospital.consultation.line",
        "consultation_id",
        string="Medicines", tracking=True
    )

    consulting_fee = fields.Float(
        string="Consulting Fee",
        tracking=True,
    )

    state = fields.Selection([
        ('new', 'New'),
        ('consultation', 'Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], default='new', string="Status", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hospital.consultation'
                ) or 'New'
    
        return super().create(vals_list)

    def action_done(self):
        self.write({
            'state': 'done'
        })


    def action_cancel(self):
        self.write({
            'state': 'cancel'
        })

    def action_consultation(self):
        self.write({
            'state': 'consultation'
        })

