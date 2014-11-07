# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from osv import fields,osv


class production_lot(osv.osv):
    _inherit = 'stock.production.lot'
    _name = 'stock.production.lot' 
    _columns = {
    'msl_status': fields.selection([('1', 'Ready'),
                                    ('2', 'Alerte'),
                                    ('3','Don t Use')],
                                    string='Msl Status', help="Ready, Alerted or Don't Use. If state is in alerted or don't use you should send the lot to baking"),
    'moisture_exposed_time': fields.float('Moisture exposed time', digits=(15,2), help="The time this specific lot has been exposed to moisture, is calculated according to the times in the related stock moves in locations with moisture."),                
      
                }

production_lot()