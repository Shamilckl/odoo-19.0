{
    'name': 'lab_management',
    'version': '19.0.1.0',
    'category': 'Healthcare',
    'summary': 'Hospital',
    'author': 'Me',
    'depends': ['base','stock','product','sale','sale_management','account','website'],

    'assets': {
        'web.assets_backend': [
            'lab_management/static/src/js/lab_menu.js',
            'lab_management/static/src/xml/lab_menu.xml',
        ],
    },

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/product_seq.xml',
        'data/appointment_seq.xml',
        'data/appointment_auto_cancel.xml',


        'views/patient_views.xml',
        'views/doctor_views.xml',
        'views/appointment_views.xml',
        'views/department_views.xml',
        'views/saleorder_views.xml',
        'views/conappointment_views.xml',
        'views/reason_views.xml',
        'views/website_form.xml',
        'views/pharmacy_views.xml',
        'views/stock_picking_views.xml',
        'views/menu.xml',

        'wizard/bookappt_views.xml',
        'wizard/productwizard_views.xml',
        'wizard/createdappointment_views.xml',

        'report/appointment_report.xml',
        'report/doctorprofile_report.xml',
        'report/appointment_xlsx.xml',
    ],
    'application': True,
}