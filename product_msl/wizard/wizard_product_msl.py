# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd.
#    (<http://www.acespritech.com>).
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
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
import time


class wizard_product_msl(osv.osv_memory):
    _name = 'wizard.product.msl'
    _columns = {
#        DR TODO: agregar campo para vista temporal 
    'last_baket_time': fields.datetime('last baket time', type='datetime',help="Ready, time between the alert."),
     
    }
_defaults = {
    'last_baket_time': lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

def save_time_msl(self, cr, user, ids, context=None):
    if context is None:
            context = {}

  
wizard_product_msl()

