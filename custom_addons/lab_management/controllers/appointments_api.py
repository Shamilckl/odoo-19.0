from odoo import http
from odoo.http import request

class AppointmentsAPI(http.Controller):

    @http.route(
        '/api/appointments',
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False
    )
    def get_appointments(self):
        appointments = request.env['lab.appointment'].search([])

        appointments_list = []

        for appointment  in appointments:
            appointments_list.append({
                'id': appointment.id,
                'patient': appointment.patient_name.patient_name,
                'phone': appointment.patient_number,
                'doctor': appointment.doctor_name.user_id.name,
                'date': appointment.consultation_date,

            })

        return request.make_json_response({
            'status': 'success',
            'appointments': appointments_list
        })