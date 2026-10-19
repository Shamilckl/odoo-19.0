from odoo import models, fields, api
from datetime import date

class LabPatient(models.Model):
    _name = 'lab.patient'
    _description = 'Lab Patient'
    _rec_name = "patient_name"

    patient_id = fields.Integer(string='Patient ID')
    patient_name = fields.Char(string='Patient Name')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(compute='_compute_age',string='Age')
    gender = fields.Selection([
                ('male', 'Male'),
                ('female', 'Female')]   
                ,string="Gender")
    phone_number = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    is_donor = fields.Boolean(string='Is Donor')
    is_test_bool = fields.Boolean(string='Is test_bool')
    # blood_group = fields.Char(string='Blood Group')
    blood_group2 = fields.Selection([
                ('a+', 'A+'),
                ('a-', 'A-'),
                ('b+', 'B+'),
                ('b-', 'B-'),
                ('ab+', 'AB+'),
                ('ab-', 'AB-'),
                ('O+', 'O+'),
                ('O-', 'O-')],
                string='Blood Group')
    active = fields.Boolean(string='Active')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()

                record.age = today.year - record.date_of_birth.year

                if(today.month,today.day)<(record.date_of_birth.month,record.date_of_birth.day):
                    record.age -=1
            else:
                record.age = 0

    @api.onchange('is_donor')
    def _onchange_is_donor(self):
        print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        if self.is_donor:
            print("fk88888888888",self.is_donor)
            self.write({
                'is_test_bool': 'True'
            })


    def action_open_appointment_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Appointment',
            'res_model': 'book.appt',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_name': self.id,
            },
        }