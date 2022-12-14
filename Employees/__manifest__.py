{
    'name':'Employees',
    'installable': True,
    'application':True,
    'auto_install':False,
    'price':99.9,
    'currency':'EUR',
    'license':'OPL-1',
    'data':[
        'security/employees_security.xml',
        'security/ir.model.access.csv',
        'view/employees_information_views.xml',
        'view/employees_department_views.xml',
        'view/employees_project_views.xml',
        'view/employees_contract_views.xml',
        'view/employees_payslip_views.xml',
        'view/employees_leave_views.xml',
        'view/employees_leave_type_views.xml',
        'view/employees_attendance_views.xml',
        'view/employees_menus.xml',
        'wizard/add_department.xml',
        'reports/employees_information_report.xml',
        'reports/employees_information_templates.xml',
        'reports/employees_payslip_report.xml',
        'reports/employees_payslip_templates.xml'
        ],
    'demo':[
        'demo/hr_department_demo.xml'
        ],
    'depends':['resource'
        ]
}