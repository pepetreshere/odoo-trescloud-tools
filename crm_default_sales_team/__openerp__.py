{
    'name' : 'Crm default Sales Team',
    'version' : '1.1',
    'author' : 'TresCloud Cia. Ltda.,Andrea García',
    'website' : 'http://trescloud.com',
    'category' : 'Crm Lead',
    'depends' : ['base','crm','sale_crm'],
    'description': """

    """,
    'data': [
        'security/ir.model.access.csv',
        'crm_lead_view.xml',
        'crm_meeting_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}