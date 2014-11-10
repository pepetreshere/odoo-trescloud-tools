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


class stock_production_lot(osv.osv):
    
    _inherit = 'stock.production.lot'
    _name = 'stock.production.lot'
    
    def _msl_calculate(self, cr, uid, ids, name, args, context=None):
        res = {}
        met, factor, open_time = 0.0, 0.0, 0.0
        for lot in self.browse(cr,uid,ids):
            if lot.moisture_exposed_time:
                met = lot.moisture_exposed_time
            if lot.product_id.msl_id:
                factor = lot.product_id.msl_id.alarm_percentage/100
            if lot.open_time:
                open_time = lot.open_time
            if met == 0.0 and factor == 0.0 and open_time == 0.0:
                res[lot.id] = 'ready'
            elif met < factor * open_time:
                res[lot.id] = 'ready'
            elif met > factor * open_time and met < open_time:
                res[lot.id] = 'alert'
            elif met >= open_time:
                res[lot.id] = 'donotuse'
        return res
    
    _MSL_STATUS=[('ready', 'Ready'),
                 ('alert', 'Alert'),
                 ('donotuse','Don\'t Use')]
    
    _columns = {
                'msl_status': fields.function(_msl_calculate, method=True, type='selection',selection=_MSL_STATUS, string='MSL Status', store=True, 
                                     help="Ready, Alerted or Don't Use. If state is in alerted or don't use you should send the lot to baking"),
                'moisture_exposed_time': fields.float('Moisture exposed time', digits=(15,2), help="The time this specific lot has been exposed to moisture, is calculated according to the times in the related stock moves in locations with moisture."),                
                'msl_id': fields.related('product_id', 'msl_id', type='many2one', relation='product.msl', string="MSL"),
                'open_time': fields.related('product_id', 'open_time', type='float', relation='product.product', string="Open Time in hours"),
                'last_baket_time': fields.datetime('last baket time', type='datetime',help="Ready, time between the alert."),
                  
                }
    
    _default = {
                'msl_status': 'ready',
                }
stock_production_lot()

class stock_partial_picking(osv.osv):
    
    _inherit = 'stock.partial.picking'
    _name = 'stock.partial.picking' 
    def onchange_prodlot_id(self, cr, uid, ids, prodlot_id, product_id, context=None):
        prod_id = self.pool.get(product_product,self).browse(cr, uid, product_id)
        if prod_id.msl_id:
            return {'value':{
                         'prodlot_id ': prodlot_id,                        
                         }
                }
        for lot in self.browse(cr, uid, prodlot_id):
            if lot.msl_status and lot.msl_status != 'ready':
                raise Exception("You must send this product lot to bake.")
        return {'value':{
                         'prodlot_id ': prodlot_id,                        
                         }
                }

stock_partial_picking()