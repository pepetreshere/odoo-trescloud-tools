# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Serpent Consulting Services (<http://www.serpentcs.com>)
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    "name" : "Sale Order Ingredients",
    "version" : "0.1",
    "description" : """ Se cambio la funcionalidad para adaptarla en SF
        Ahora los productos asociados a la receta salen con precio 0.0
        """,
    "author" : "Serpent Consulting Services Pvt. Ltd.",
    "website" : "http://www.serpentcs.com",
    "depends" : ['sale','mrp','product_visible_discount'],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
        'sale_ingredients_view.xml',
        'wizard/expand_bom_message_view.xml'
    ],
    "auto_install": False,
    "installable": True,
}
