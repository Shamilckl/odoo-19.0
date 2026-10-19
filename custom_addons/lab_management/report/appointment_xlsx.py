from odoo import models


class AppointmentXlsx(models.AbstractModel):
    _name = 'report.lab_management.appointment_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        bold = workbook.add_format({
            'bold': True,
            'font_size': 12,
        })

        sheet = workbook.add_worksheet('Appointments')

        sheet.write(0, 1, 'Patient', bold)
        sheet.write(0, 2, 'Phone Number', bold)
        sheet.write(0, 3, 'Doctor', bold)
        sheet.write(0, 4, 'Consultation Date', bold)

        row = 1

        for appointment in lines:

            sheet.write(row, 1,appointment.patient_name.patient_name or '')
            sheet.write(row, 2,appointment.patient_number or '')
            sheet.write(row, 3,appointment.doctor_name.user_id.name or '')
            sheet.write(row, 4, str(appointment.consultation_date or ''))

            row += 1