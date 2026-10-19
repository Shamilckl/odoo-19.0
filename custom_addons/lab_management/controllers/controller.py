from odoo import http
from odoo.http import request


class AppointmentForm(http.Controller):

    @http.route(
        '/appointment_click',
        type='http',
        auth='public',
        website=True
    )
    def appaction(self, **kwargs):
        return request.render('lab_management.appointment_click',{})

    @http.route(
        '/appointment_page',
        type='http',
        auth='public',
        website=True,
        methods=['POST']
    )
    def appform(self, **kwargs):
        patient = request.env['lab.patient'].sudo().create({
            'patient_name': kwargs.get('patient_name'),
            'email': kwargs.get('email'),
            'phone_number': kwargs.get('phone_number'),
        })

        doctor_id = int(kwargs.get('doctor_name'))

        request.env['lab.appointment'].sudo().create({
            'patient_name': patient.id,
            'patient_number':kwargs.get('patient_number'),
            'doctor_name': doctor_id,
        })

        return request.render('lab_management.appointment_thank_you_template',{})
