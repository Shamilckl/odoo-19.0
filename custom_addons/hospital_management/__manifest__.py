{
    'name': 'Hospital Management',
    'version': '19.0.1.0',
    'category': 'Healthcare',
    'summary': 'Hospital',
    'author': 'Me',
    'depends': ['base','stock','product','mail','sale','sale_management'],

    'data': [
        'security/ir.model.access.csv',

        'data/consultation_seq.xml',
        'data/appointment_seq.xml',
        'data/patient_seq.xml',

        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
        'views/consultation_views.xml',
        'views/hospital_slot_views.xml',
        'views/product_views.xml',
        'views/menu.xml',

        'report/appointment_report.xml',
        'report/consultation_report.xml',
        'report/report.xml',


    ],
    'application': True,
}