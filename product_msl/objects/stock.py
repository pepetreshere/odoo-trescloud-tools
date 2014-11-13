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

from __future__ import division
from openerp.osv import fields, orm, osv
from openerp.tools.translate import _
import time
from datetime import *
import math
from openerp.tools import float_compare

import pytz

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
        moisture_exposed_time = 0.0
        move_pool = self.pool.get('stock.move')
        move_ids = move_pool.search(cr, uid, [('prodlot_id', 'not in', [0.0])],context=context)
        for lot in self.browse(cr,uid,ids):
            for move_id in move_ids:
                move = move_pool.browse(cr,uid,move_id)
                if lot == move.prodlot_id:
                    moisture_exposed_time += move.duration 
            res[lot.id] = moisture_exposed_time
        return res
    
    def _get_by_moves(self, cr, uid, ids, context=None):
        lot_ids = []
        for lot in self.browse(cr, uid, ids, context=context):
                lot_ids.append(lot.id) 
        return lot_ids

    _store_rules = {
                    'stock.production.lot': (_get_by_moves, ['moisture_exposed_time', 'msl_id','open_time'], 20),
                    }

    _columns = {
                'msl_status': fields.function(_msl_calculate, 
                                              method=True, 
                                              type='selection', 
                                              selection=_MSL_STATUS, 
                                              string='MSL Status', 
                                              store=_store_rules, 
                                              help="Ready, Alerted or Don't Use. If state is in alerted or don't use you should send the lot to baking"),
                'moisture_exposed_time': fields.function(_moisture_exposed_time_calculate, method=True, type='float', string='Moisture exposed time', digits=(15,2), store=True,
                                                         help="The time this specific lot has been exposed to moisture, is calculated according to the times in the related stock moves in locations with moisture."),                
                'msl_id': fields.related('product_id', 'msl_id', type='many2one', relation='product.msl', string="MSL"),
                'open_time': fields.related('product_id', 'open_time', type='float', relation='product.product', string="Open Time in hours"),
                'last_baket_time': fields.datetime('Last Baked Time', type='datetime',help="Ready, time between the alert."),                
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
    
    def float_time_convert(self, float_val):
        hours = math.floor(abs(float_val))
        mins = abs(float_val) - hours
        mins = round(mins * 60)
        if mins >= 60.0:
            hours = hours + 1
            mins = 0.0
        float_time = '%02d:%02d' % (hours,mins)
        return float_time

    def float_to_datetime(self, float_val):
        str_float = self.float_time_convert(float_val)
        hours = int(str_float.split(':')[0])
        minutes = int(str_float.split(':')[1])
        days = 1
        if hours / 24 > 0:
            days += hours / 24
            hours = hours % 24
        return datetime(1900, 1, int(days), hours, minutes)

    def float_to_timedelta(self, float_val):
        str_time = self.float_time_convert(float_val)
        return timedelta(0, int(str_time.split(':')[0]) * 60.0*60.0
            + int(str_time.split(':')[1]) * 60.0)
    
    def total_seconds(self, td):
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6     

    def _get_expose_duration(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        active_tz = pytz.timezone(context.get("tz","UTC") if context else "UTC")
        move_pool = self.pool.get('stock.move')
        str_now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        for move_id in ids:
            duration = 0.0
            move = self.browse(cr, uid, move_id, context=context)
            res[move.id] = {}
            # 2012.10.16 LF FIX : Attendance in context timezone
            move_begin = datetime.strptime(
                move.date, '%Y-%m-%d %H:%M:%S'
                ).replace(tzinfo=pytz.utc).astimezone(active_tz)
            next_move_date = str_now
            next_move_ids = False
            # should we compute for sign out too?
            if move.location_dest_id:
                next_move_ids = self.search(cr, uid, [
                                                      ('state', '!=', 'draft'),
                                                      ('location_id', '=', move.location_dest_id.id),
                                                      ('prodlot_id', 'not in', [0.0]),
                                                      ('date', '<', move.date)], order='date', context=context)
                for next_move_id in next_move_ids:
                    next_move = self.browse(cr, uid, next_move_id, context=context)
                    if next_move.prodlot_id == move.prodlot_id:
                        next_move_date = next_move.date
                # 2012.10.16 LF FIX : Attendance in context timezone
                move_end = datetime.strptime(
                    next_move_date, '%Y-%m-%d %H:%M:%S'
                    ).replace(tzinfo=pytz.utc).astimezone(active_tz)
                duration_delta = move_end - move_begin
                duration = self.total_seconds(duration_delta) / 60.0 / 60.0
            res[move.id]['duration'] = duration
            res[move.id]['end_datetime'] = next_move_date
        return res

    def _get_by_location(self, cr, uid, ids, context=None):
        move_ids = []
        move_pool = self.pool.get('stock.move')
        for location in self.browse(cr, uid, ids, context=context):
            movement_ids = move_pool.search(cr, uid, 
                                            [('location_dest_id', '=', location.id),
                                             ('state', '!=', 'done')], 
                                            context=context)
            for move_id in movement_ids:
                if move_id not in move_ids:
                    move_ids.append(move_id)
        return move_ids

    def _get_by_moves(self, cr, uid, ids, context=None):
        move_ids = []
        for move in self.browse(cr, uid, ids, context=context):
            if move.location_dest_id and move.location_dest_id.hasmoisture and move.id not in move_ids:
                move_ids.append(move.id) 
        return move_ids

    _store_rules = {
                    'stock.move': (_get_by_moves, ['prodlot_id', 'dummy_field','location_dest_id'], 20),
                    'stock.location': (_get_by_location, ['hasmoisture'], 20),
                    }

    _columns = {
        'duration': fields.function(_get_expose_duration, method=True, multi='duration', string="Attendance duration",
            store=_store_rules),
        'end_datetime': fields.function(_get_expose_duration, method=True, multi='duration', type="datetime", string="End date time",
            store=_store_rules),
        'dummy_field': fields.char('Dummy field',help="Used to cause a write that updates the stored function fields")
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
        message=''
        if warning and warning['warning'] and warning['warning']['message']:
                    message = warning['warning']['message']
        if not prodlot_id:
            return {'warning': warning}
        product_obj = self.pool.get('product.product')
        product_id = product_obj.browse(cr, uid, product_id, context)
        prodlot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id, context)
        if product_id.msl_id:
            if prodlot and prodlot.msl_status and prodlot.msl_status != 'ready':
                
                warning = {
                           'title': 'Warning!',
                           'message': message + "\nYou must send this product lot to bake."
                }
                return {'warning': warning}
        if warning is {}:
            return {'warning': warning}
        else:
            return warning
    
stock_move()

class stock_location(osv.osv):
    
    _inherit = 'stock.location'
    _name = 'stock.location'
    
    _columns = {
            'hasmoisture':fields.boolean('Has Moisture', required=False, help='Check this, if the location has moisture.'),
                    }
stock_location()
