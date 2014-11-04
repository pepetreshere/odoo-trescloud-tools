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

import datetime
import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from string import digits
  
     
class product_msl(osv.osv):
     _name = "product.msl"   
     _columns = {
        'name': fields.char('Zone Name', size=60, required=True, 
                            help='Name of the MSL.'),
        'packagend_time': fields.float('Packaging Time in hours',digits=(15,2), size=40,help="shelf life in sealed bag.", required=True),
        'open_time': fields.float('Open Time in hours', digits=(15,2),size=40, help="time I open the package",required=True),
        'alarm_percentage': fields.float('Alarm percentage', digits=(15,2),size=40, help="percentage of moisture alarm ",required=True)
           }

    

  




  
   
  