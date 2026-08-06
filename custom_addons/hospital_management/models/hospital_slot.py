from odoo import models, fields, api

class HospitalSlot(models.Model):
    _name = "hospital.slot"
    _description = "Appointment Slot"
    _rec_name = "name"

    name = fields.Char(
        string="Slot",
        compute="_compute_name",
        store=True
    )

    start_time = fields.Float(string="Start Time", required=True)

    start_period = fields.Selection([
        ('am','AM'),
        ('pm','PM'),
    ])


    end_time = fields.Float(string="End Time", required=True)

    end_period = fields.Selection([
        ('am', 'AM'),
        ('pm', 'PM'),
    ])

    @api.depends(
        'start_time',
        'start_period',
        'end_time',
        'end_period'
    )
    def _compute_name(self):
        for rec in self:
            start_period = (rec.start_period or "").upper()
            end_period = (rec.end_period or "").upper()

            rec.name = (
                f"{rec.start_time:.2f} {start_period} - "
                f"{rec.end_time:.2f} {end_period}"
            )