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

from openerp.osv import fields,osv


class stock_production_lot(osv.osv):
    
    _inherit = 'stock.production.lot'
    _name = 'stock.production.lot'
    _MSL_STATUS=[('ready', 'Ready'),
             ('alert', 'Alert'),
             ('donotuse','Don\'t Use')]

    def name_get(self, cr, uid, ids, context=None):
        result = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            for status in self._MSL_STATUS:
                if status[0] == record.msl_status:
                    name +=  ' [' + status[1] + ']'
            result.append((record.id,name)) #, '+states[session.state]+')'))
        return result
    
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
    
    def _moisture_exposed_time_calculate(self, cr, uid, ids, name, args, context=None):
        res = {}
        stock_move_ids = self.pool.get('stock.move').search(cr, uid, [('')])
        location_id = self.pool.get('stock.location').browse(cr, uid, product_id)
        for lot in self.browse(cr,uid,ids):
            res[lot.id] = 0.0
        return res
    
    _columns = {
                'msl_status': fields.function(_msl_calculate, method=True, type='selection', selection=_MSL_STATUS, string='MSL Status', store=True, 
                                     help="Ready, Alerted or Don't Use. If state is in alerted or don't use you should send the lot to baking"),
                'moisture_exposed_time': fields.function(_moisture_exposed_time_calculate, method=True, type='float', string='Moisture exposed time', digits=(15,2), store=True,
                                                         help="The time this specific lot has been exposed to moisture, is calculated according to the times in the related stock moves in locations with moisture."),                
                'msl_id': fields.related('product_id', 'msl_id', type='many2one', relation='product.msl', string="MSL"),
                'open_time': fields.related('product_id', 'open_time', type='float', relation='product.product', string="Open Time in hours"),
                'last_baket_time': fields.datetime('last baket time', type='datetime',help="Ready, time between the alert."),
                  
                }
    
    _default = {
                'msl_status': 'ready',
                }
stock_production_lot()

class stock_partial_picking(osv.osv):
    
    _inherit = 'stock.partial.picking.line'
    _name = 'stock.partial.picking.line' 
    def onchange_prodlot_id(self, cr, uid, ids, prodlot_id, product_id, context=None):
        prod_id = self.pool.get('product.product').browse(cr, uid, product_id)
        lot = False
        if prod_id.msl_id:
            if prodlot_id:
                    lot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id)
            if lot:
                if lot.msl_status and lot.msl_status != 'ready':
                    warning = {
                               'title': 'Warning Production',
                               'message': "You must send this product lot to bake."
                    }
                    value = {'prodlot_id': prodlot_id}
                    return {'warning': warning, 'value': value }
            else:
                return {'value':{'prodlot_id ': prodlot_id,}
                }

stock_partial_picking()

class stock_move(osv.osv):
    
    _inherit = 'stock.move'
    _name = 'stock.move' 
    
    def _number_of_hours_used(self, cr, uid, ids, name, args, context=None):
        res = {}
        for move in self.browse(cr,uid,ids):
            if move.moisture_exposed_time:
                met = move.moisture_exposed_time
            if move.product_id.msl_id:
                factor = move.product_id.msl_id.alarm_percentage/100
            if move.open_time:
                open_time = move.open_time
            if met == 0.0 and factor == 0.0 and open_time == 0.0:
                res[move.id] = 'ready'
            elif met < factor * open_time:
                res[move.id] = 'ready'
            elif met > factor * open_time and met < open_time:
                res[move.id] = 'alert'
            elif met >= open_time:
                res[move.id] = 'donotuse'
        return res
    
    _columns = {
            'number_of_hours_used': fields.function(_number_of_hours_used,
                                                    type='float', string='Number of hours used', store=True, 
                                                    help="Ready, Alerted or Don't Use. If state is in alerted or don't use you should send the lot to baking",   
                                                    digits_compute=dp.get_precision('Product Unit of Measure')),
                    }
                                   
    def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False,
                        loc_id=False, product_id=False, uom_id=False, context=None):
        """ On change of production lot gives a warning message.
        @param prodlot_id: Changed production lot id
        @param product_qty: Quantity of product
        @param loc_id: Location id
        @param product_id: Product id
        @return: Warning message
        """
        warning = super(stock_move,self).onchange_lot_id(cr, uid, ids, prodlot_id, product_qty,
                        loc_id, product_id, uom_id, context)
        if not prodlot_id:
            return {'warning': warning}
        product_obj = self.pool.get('product.product')
        product_id = product_obj.browse(cr, uid, product_id, context)
        prodlot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id, context)
        if product_id.msl_id:
            if prodlot and prodlot.msl_status and prodlot.msl_status != 'ready':
                warning = {
                           'title': 'Warning!',
                           'message': warning['warning']['message'] + "\nYou must send this product lot to bake."
                }
        return {'warning': warning}
    
stock_move()

class stock_location(osv.osv):
    
    _inherit = 'stock.location'
    _name = 'stock.location'
    
    _columns = {
            'hasmoisture':fields.boolean('Has Moisture', required=False, help='Check this, if the location has moisture.'),
                    }
stock_location()
