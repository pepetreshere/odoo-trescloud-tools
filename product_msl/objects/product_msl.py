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
from lxml import etree
import math
import pytz
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
class product_msl(osv.osv):
    _name = "product.msl"
    _columns = {
    'name': fields.char('Name', size=50, required=True, help='Name of the MSL.'),
    'packaged_time': fields.float('Packaged  life time in hours',digits=(15,2), size=40,help="Lifetime of the component when sealed", required=True),
    'open_time': fields.float('Max time exposed to moisture', digits=(15,2),size=40, help="Maximun period of time in which the component must be mounted and reflowed",required=True),
    'alarm_percentage': fields.float('Alarm percentage', digits=(15,2),size=40, help="Percentage of time exposed to moisture at which the component gets alarmed as follows: Orange (Alarmed. should be sent to baking), Red (Moisture exceeded, do not use)",required=True),
                }
    _defaults = {  
        'alarm_percentage': 75.0,  
        }
product_msl()
                
   
   
    

  




  
   
  