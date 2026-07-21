{
    'name': 'Hospital Management',
    'version': '19.0.1.0',
    'category': 'Healthcare',
    'summary': 'Hospital',
    'author': 'Me',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/room_views.xml',
        'views/medicine_views.xml',
        'views/laboratory_views.xml',
        'views/appointment_views.xml',
        'views/billing_views.xml',
        'views/menu.xml',

        'report/appointment_report.xml',
        'report/billing_report.xml',
        'report/report.xml',
    ],
    'application': True,
}