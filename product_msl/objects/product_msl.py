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

import openerp
from openerp.osv import osv, fields
from openerp.tools.translate import _


class product_msl(osv.osv):
    _name = "product.msl"
    _inherit = ['mail.thread']
    
    def _calculate_alert_time(self, cr, uid, ids, name, args, context=None):
        res = {}
        factor, open_time = 0.0, 0.0
        for product_msl in self.browse(cr,uid,ids):
            if product_msl.alarm_percentage:
                factor = product_msl.alarm_percentage/100
            if product_msl.open_time:
                open_time = product_msl.open_time
            res[product_msl.id] = factor * open_time
        return res
    
    _columns = {
    'name': fields.char('Name', size=50, required=True, help='Name of the MSL.'),
    'control': fields.boolean('Is not Controlled', required=False, help='Check this field if the MSL is not controlled, this means this lot won\'t deteriorate on locations with moisture.', track_visibility='onchange'), 
    'packaged_time': fields.float('Packaging Time in hours',digits=(15,2), size=40,help="Lifetime of the component when saled in hours.", required=True, track_visibility='onchange'),
    'open_time': fields.float('Open Time in hours', digits=(15,2),size=40, help="Maximiun period of time in which the component must be mounted and used.",required=True, track_visibility='onchange'),
    'alarm_percentage': fields.float('Alarm percentage', digits=(15,2),size=40, help="Percentage of moisture at which the item gets alarmed as follows: Orange (Alarmed. should be sent to baking), Red (Moisture exceeded, do not use)",required=True, track_visibility='onchange'),
    'time_alert': fields.function(_calculate_alert_time, method=True, type='float', string='Alert Time in hours', help="Alert time period in which the component should be taken into consideration to send baking."), 
    'comment': fields.text('Additional Information'),
                }
    _defaults = {  
        'alarm_percentage': 75.0,  
        }
    
        
    def unlink(self, cr, uid, ids, context=None):
        msl_ids = self.pool.get('product.product').search(cr, uid, [('msl_id','=',ids[0])], context=context)
        if msl_ids:
            raise osv.except_osv(_('Invalid Action!'), _('In order to delete a MSL, you must first unlink the MSL from the products related.'))
        else:
            osv.osv.unlink(self, cr, uid, ids, context=context)
        return True
    
    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}
        if not default:
            default = {}
        product = self.read(cr, uid, id, ['name'], context=context)
        default = default.copy()
        default.update(name=_("%s (copy)") % (product['name']))
        return super(product_msl, self).copy(cr, uid, id, default=default,
                    context=context)
product_msl()
  