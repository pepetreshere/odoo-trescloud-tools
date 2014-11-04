# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source TRESCloud
#    Copyright (c) 2014-TRESCloud S.A. (<http://www.trescloud.com>).
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
    'name': 'Product Msl',
    'version': '1.0',
    'category': 'warehouse',
    'depends': ['base','mpr'
                ],
    'author': 'TRESCLOUD Henry Granada',
    'description': 
    """
    Resumen:
    sensivilidad a la humedad Humedad de niveles
    Funciones:
 Manejo de Directrices
Los efectos perjudiciales de la humedad absorbida en paquetes de semiconductores durante el montaje SMT
Identificar áreas de potencial preocupación para  los usuarios y los pasos que deben tomar para evitar problemas. 
    Authors: 
   Henry Granada
    TRESCLOUD Cia Ltda
    """,
    'website': 'http://www.trescloud.com',
    'data': [
        'views/res_partner_view.xml',
       # 'security/',
    ],
    'installable': True,
    'auto_install': False,
}
