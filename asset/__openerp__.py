# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 CodUP (<http://codup.com>).
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
    'name': 'Assets',
    'version': '1.1',
    'summary': 'Asset Management',
    'description': """
Managing assets in OpenERP.
===========================
Support location for assets.
Support assign asset to employee.
Author: Pablo Vizhnay
    """,
    'author': 'TRESCLOUD CIA. LTDA',
    'website': 'www.trescloud.com',
    'category': 'Enterprise Asset Management',
    'images': ['images/assets.png'],
    'depends': ['base', 'stock', 'account_asset','hr'],
 
    'data': [
        'security/asset_security.xml',
        'security/ir.model.access.csv',
        'asset_view.xml',
  
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: