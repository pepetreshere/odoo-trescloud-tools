{
    'name' : 'Partner related with Meeting,PhoneCall,Opportunity',
    'version' : '1.1',
    'author' : 'TresCloud Cia. Ltda.,Andrea García',
    'website' : 'http://openerp.com',
    'category' : 'Marketing',
    'depends' : ['base','crm'],
    'description': """
     Show partner relation with Opportunity, Meeting, Phonecalls
    """,
    'data': [
        'res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': True,
}
