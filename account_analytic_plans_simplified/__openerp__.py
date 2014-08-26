# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd. (<http://acespritech.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Simplified Analytic Plans',
    'version': '1.0',
    'category': 'account',
    'depends': ['base','account_analytic_plans'],
    'author': 'TRESCLOUD Cia Ltda',
    'description': 
    """
    1. Simplifies the analytic plans, allows the user to distribute an account entry into
    several analytic accounts, but without the need of creating analytic plans.
    2. Removes advanced fields, menus and reports from the analytic plans module
    3. Automaticall sets the name of an analytic plan like this: 70% Admin, 20% Projects, 10% Projects/Project A  
        
    Authors: 
    Andres Calle
    TRESCLOUD Cia Ltda
    """,
    'website': 'http://www.trescloud.com',
    'data': [
             'views/account_analytic_plan_instance_view.xml',
             'views/account_analytic_plans_no_replace_view.xml',
             
    ],
    'installable': True,
    'auto_install': False,
}
