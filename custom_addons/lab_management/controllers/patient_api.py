from odoo import http
from odoo.http import request


class PatientAPI(http.Controller):

    @http.route(
        '/api/patients',
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False
    )
    def get_patients(self):
        patients = request.env['lab.patient'].search([])

        patient_list = []

        for patient in patients:
            patient_list.append({
                'id': patient.id,
                'name': patient.patient_name,
                'age': patient.age,
                'gender': patient.gender,
                'phone': patient.phone_number,
            })

        return request.make_json_response({
            'status': 'success',
            'patients': patient_list
        })