from osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class fleet_type_vehicle(osv.Model):
 
    _name = 'fleet.type.vehicle'
 
    _columns = {
        'name': fields.char('Type vehicle', size=64),
        'type_ids': fields.one2many('fleet.vehicle', 'type_id', 'Type vehicle'),
            }

class fleet_vehicle(osv.osv):
    _inherit = 'fleet.vehicle'

    def _get_odometer(self, cr, uid, ids, odometer_id, arg, context):
        v = super(fleet_vehicle,self)._get_odometer(cr, uid, ids, odometer_id, arg, context=context)
        return v 
    
    def _set_odometer(self, cr, uid, id, name, value, args=None, context=None):
         if value:
            date = fields.date.context_today(self, cr, uid, context=context)
            driver_id = self.browse(cr, uid, id, context=context).driver_id
            data = {'value': value, 'date': date, 'vehicle_id': id, 'driver_id':driver_id.id}
            return self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
           
    _columns={
              'odometer': fields.function(_get_odometer, fnct_inv=_set_odometer, type='float', string='Last Odometer', help='Odometer measure of the vehicle at the moment of this log'),
              'motor_sn': fields.char('Engine Number', size=32, help='Unique number written on the vehicle motor (engine number)'),
              'no_vehicle': fields.integer('Number Vehicle', size=32),
              'year': fields.integer('Manufacturing year', size=32),
              'type_id': fields.many2one('fleet.type.vehicle','Types vehicle'),
              'vehicle_registration': fields.char('Vehicle Registration', size=32, help='License plate number of the vehicle (ie: vehicle registration for a car)'),
              'mobile': fields.char('Movil'),
              'image_vehicle': fields.binary("Photo Vehicle front", help="This field holds the image used as photo, limited to 1024x1024px."),
              'description': fields.char('Photo Description', size=40,),
              'image_vehicle1': fields.binary("Photo Vehicle Back", help="This field holds the image used as photo, limited to 1024x1024px."),
              'description1': fields.char('Photo Description', size=40,),
              'image_vehicle2': fields.binary("Photo Vehicle Other", help="This field holds the image used as photo, limited to 1024x1024px."),
              'description2': fields.char('Photo Description', size=40,),
              'image_vehicle3': fields.binary("Photo Vehicle Other", help="This field holds the image used as photo, limited to 1024x1024px."),
              'description3': fields.char('Photo Description', size=40,),
        }
    def on_change_contact(self, cr, uid, ids, driver_id, context=None):
        """ When changing the user, also set a section_id or restrict section id
            to the ones driver_id mobile. """
        values = {}
        if driver_id:
            partner = self.pool.get('res.partner').browse(cr, uid, driver_id, context=context)
            values = {
                'mobile' : partner.mobile,
            }
        return {'value' : values}
    
    def on_change_odometer(self, cr, uid, ids, odometer, context=None):
        if context is None:
            context = {}
        vals = {}
        if ids:
            for vehicle in self.browse(cr, uid, ids, context):
                old_odometer = vehicle.odometer
                if old_odometer > odometer:
                    raise osv.except_osv(_('Invalid action!'), 
                                         _('The new reading should be greater than or equal to the accumulated read for this equipment.'))
                vals.update({'odometer': odometer})
        return vals
    
    def create(self, cr, uid, data, context=None):
        vehicle_id = super(fleet_vehicle, self).create(cr, uid, data, context=context)
        vehicle = self.browse(cr, uid, vehicle_id, context=context)
        self.message_post(cr, uid, [vehicle_id], body=_('Vehicle %s has been added to the fleet!') % (vehicle.license_plate), context=context)
        return vehicle_id
    
    def write(self, cr, uid, ids, vals, context=None):
        """
        This function write an entry in the openchatter whenever we change important information
        on the vehicle like the model, the drive, the state of the vehicle or its license plate
        """
        for vehicle in self.browse(cr, uid, ids, context):
            changes = []
            if 'model_id' in vals and vehicle.model_id.id != vals['model_id']:
                value = self.pool.get('fleet.vehicle.model').browse(cr,uid,vals['model_id'],context=context).name
                oldmodel = vehicle.model_id.name or _('None')
                changes.append(_("Model: from '%s' to '%s'") %(oldmodel, value))
            if 'driver_id' in vals and vehicle.driver_id.id != vals['driver_id']:
                value = self.pool.get('res.partner').browse(cr,uid,vals['driver_id'],context=context).name
                olddriver = (vehicle.driver_id.name) or _('None')
                changes.append(_("Driver: from '%s' to '%s'") %(olddriver, value))
            if 'odometer' in vals and vehicle.odometer != vals['odometer']:
                old_odometer = vehicle.odometer or _('None')
                if old_odometer >= vals['odometer']:
                    raise osv.except_osv(_('Invalid action!'), _('The date Value is not valid because is less than the last Value for the odometer'))
                else:
                    changes.append(_("Odometer: from '%s' to '%s'") %(old_odometer, vals['odometer']))
            if 'state_id' in vals and vehicle.state_id.id != vals['state_id']:
                value = self.pool.get('fleet.vehicle.state').browse(cr,uid,vals['state_id'],context=context).name
                oldstate = vehicle.state_id.name or _('None')
                changes.append(_("State: from '%s' to '%s'") %(oldstate, value))
            if 'license_plate' in vals and vehicle.license_plate != vals['license_plate']:
                old_license_plate = vehicle.license_plate or _('None')
                changes.append(_("License Plate: from '%s' to '%s'") %(old_license_plate, vals['license_plate']))
              
            if len(changes) > 0:
                self.message_post(cr, uid, [vehicle.id], body=", ".join(changes), context=context)

#        vehicle_id = super(fleet_vehicle,self).write(cr, uid, ids, vals, context)
        vehicle_id = super(fleet_vehicle,self).write(cr, uid, ids, vals, context)
        return True
    
fleet_vehicle()

class trescloud_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns={
              'contractor': fields.boolean('Contractor', help="Check this box if this contact is a Contractor. If it's not checked."),
              'driver': fields.boolean('Driver', help="Check this box if this contact is a Driver. If it's not checked."),
            }
    _defaults = {
              #'function': 'Conductor',
            }
trescloud_partner()
class fleet_vehicle_cost(osv.Model):
    _inherit = 'fleet.vehicle.cost'

    _columns = {
        'amount': fields.float('Total Price',digits_compute=dp.get_precision('Fleet'),),
        }
fleet_vehicle_cost()    

class fleet_vehicle_log_contract(osv.Model):
    _inherit = ["mail.thread","fleet.vehicle.log.contract"]
    _name = 'fleet.vehicle.log.contract'

    def _get_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.odometer_id:
                res[record.id] = record.odometer_id.value
        return res
      
    def _set_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'), _('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id, context=context).date
        if not(date):
            date = fields.date.context_today(self, cr, uid, context=context)
        data_aux = self.browse(cr, uid, id, context=context)       
        data = {'value': value, 'date': date, 'vehicle_id': data_aux.vehicle_id.id, 'driver_id': data_aux.purchaser_id.id}
        return self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        #return self.write(cr, uid, id, {'odometer_id': odometer_id}, context=context)

            
    def write(self, cr, uid, ids, vals, context=None):
        """
        This function write an entry in the openchatter whenever we change important information
        on the vehicle like the model, the drive, the state of the vehicle or its license plate
        """
        for vehicle in self.browse(cr, uid, ids, context):
            changes = []
#            if 'model_id' in vals and vehicle.model_id.id != vals['model_id']:
#                value = self.pool.get('fleet.vehicle.model').browse(cr,uid,vals['model_id'],context=context).name
#                oldmodel = vehicle.model_id.name or _('None')
#                changes.append(_("Model: from '%s' to '%s'") %(oldmodel, value))
            if 'date' in vals and vehicle.date != vals['date']:
                old_date = vehicle.date or _('None')
                changes.append(_("Date: from '%s' to '%s'") %(old_date, vals['date']))
            if 'odometer' in vals and vehicle.odometer != vals['odometer']:
                old_odometer = vehicle.odometer or _('None')
                if old_odometer >= vals['odometer']:
                    raise osv.except_osv(_('Invalid action!'), _('The date Value is not valid because is less than the last Value for the odometer'))
                else:
                    changes.append(_("Odometer: from '%s' to '%s'") %(old_odometer, vals['odometer']))

            if len(changes) > 0:
                self.message_post(cr, uid, [vehicle.id], body=", ".join(changes), context=context)

        vehicle_id = super(fleet_vehicle_log_contract,self).write(cr, uid, ids, vals, context)
        return True
    _columns = {
        'odometer': fields.function(_get_odometer, fnct_inv=_set_odometer, type='float', string='Odometer Value', help='Odometer measure of the vehicle at the moment of this log'),
    }  
    
class fleet_vehicle_log_fuel(osv.Model):
 
    _name = 'fleet.vehicle.log.fuel'
    _inherit = ['fleet.vehicle.log.fuel']

    def _get_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.odometer_id:
                res[record.id] = record.odometer_id.value
        return res
      
    def _set_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'), _('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id, context=context).date
        if not(date):
            date = fields.date.context_today(self, cr, uid, context=context)
        data_aux = self.browse(cr, uid, id, context=context)       
        data = {'value': value, 'date': date, 'vehicle_id': data_aux.vehicle_id.id, 'driver_id': data_aux.purchaser_id.id}
        return self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        #return self.write(cr, uid, id, {'odometer_id': odometer_id}, context=context)
        
    _columns = {
        'odometer': fields.function(_get_odometer, fnct_inv=_set_odometer, type='float', string='Odometer Value', help='Odometer measure of the vehicle at the moment of this log'),
        'liter': fields.float('Gallon',digits_compute=dp.get_precision('Fleet'),),
        'price_per_liter': fields.float('Price Per Gallon',digits_compute=dp.get_precision('Fleet'),),
        'fuel_type': fields.selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle'),
        'gasoline_type': fields.selection([('super', 'Super'), ('extra', 'Extra')], 'Gasoline Type'),
        'cost_amount': fields.related('cost_id', 'amount', string='Amount', type='float', store=True,track_visibility='always'), #we need to keep this field as a related with store=True because the graph view doesn't support (1) to address fields from inherited table and (2) fields that aren't stored in database
    }
    
    def on_change_liter(self, cr, uid, ids, liter, price_per_liter, amount, context=None):
        #need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        #make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        #liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        #of 3.0/2=1.5)
        #If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
        #onchange. And in order to verify that there is no change in the result, we have to limit the precision of the 
        #computation to 2 decimal
        obj_decimal=self.pool.get('decimal.precision') 
        decimals=obj_decimal.search(cr,uid,[('name','=','Fleet')])
        digit=2
        if decimals:
            digit=obj_decimal.browse(cr,uid,decimals)[0].digits
        liter = float(liter)
        price_per_liter = float(price_per_liter)
        amount = float(amount)
        if liter > 0 and price_per_liter > 0 and round(liter*price_per_liter,digit) != amount:
            return {'value' : {'amount' : round(liter * price_per_liter,digit),}}
        elif amount > 0 and liter > 0 and round(amount/liter,digit) != price_per_liter:
            return {'value' : {'price_per_liter' : round(amount / liter,digit),}}
        elif amount > 0 and price_per_liter > 0 and round(amount/price_per_liter,digit) != liter:
            return {'value' : {'liter' : round(amount / price_per_liter,digit),}}
        else :
            return {}
        
    def on_change_price_per_liter(self, cr, uid, ids, liter, price_per_liter, amount, context=None):
        #need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        #make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        #liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        #of 3.0/2=1.5)
        #If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
        #onchange. And in order to verify that there is no change in the result, we have to limit the precision of the 
        #computation to 2 decimal
        obj_decimal=self.pool.get('decimal.precision') 
        decimals=obj_decimal.search(cr,uid,[('name','=','Fleet')])
        digit=2
        if decimals:
            digit=obj_decimal.browse(cr,uid,decimals)[0].digits
        liter = float(liter)
        price_per_liter = float(price_per_liter)
        amount = float(amount)
        if liter > 0 and price_per_liter > 0 and round(liter*price_per_liter,digit) != amount:
            return {'value' : {'amount' : round(liter * price_per_liter,digit),}}
        elif amount > 0 and price_per_liter > 0 and round(amount/price_per_liter,digit) != liter:
            return {'value' : {'liter' : round(amount / price_per_liter,digit),}}
        elif amount > 0 and liter > 0 and round(amount/liter,digit) != price_per_liter:
            return {'value' : {'price_per_liter' : round(amount / liter,digit),}}
        else :
            return {}

    def on_change_amount(self, cr, uid, ids, liter, price_per_liter, amount, context=None):
        #need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        #make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        #liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        #of 3.0/2=1.5)
        #If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
        #onchange. And in order to verify that there is no change in the result, we have to limit the precision of the 
        #computation to 2 decimal
        obj_decimal=self.pool.get('decimal.precision') 
        decimals=obj_decimal.search(cr,uid,[('name','=','Fleet')])
        digit=2
        if decimals:
            digit=obj_decimal.browse(cr,uid,decimals)[0].digits
        liter = float(liter)
        price_per_liter = float(price_per_liter)
        amount = float(amount)
        if amount > 0 and liter > 0 and round(amount/liter,digit) != price_per_liter:
            return {'value': {'price_per_liter': round(amount / liter,digit),}}
        elif amount > 0 and price_per_liter > 0 and round(amount/price_per_liter,digit) != liter:
            return {'value': {'liter': round(amount / price_per_liter,digit),}}
        elif liter > 0 and price_per_liter > 0 and round(liter*price_per_liter,digit) != amount:
            return {'value': {'amount': round(liter * price_per_liter,digit),}}
        else :
            return {}
    
    def on_change_fuel_type(self, cr, uid, ids, vehicle_id, context=None):
        """ When changing the user, also set a section_id or restrict section id
            to the ones vehicle_id fuel pype. """
        values = {}
        if vehicle_id:
            vehicle = self.pool.get('fleet.vehicle').browse(cr, uid, vehicle_id, context=context)
            values = {
                'fuel_type' : vehicle.fuel_type,
            }
        return {'value' : values}
        
class fleet_vehicle_odometer(osv.Model):
    
    _inherit='fleet.vehicle.odometer'

    def on_change_vehicle(self, cr, uid, ids, vehicle_id, context=None):
        if not vehicle_id:
            return {}
        odometer_unit = self.pool.get('fleet.vehicle').browse(cr, uid, vehicle_id, context=context).odometer_unit
        driver = self.pool.get('fleet.vehicle').browse(cr, uid, vehicle_id, context=context).driver_id
        return {
            'value': {
                'unit': odometer_unit,
                'driver_id': driver.id,
            }
        }

    _columns = {
        'driver_id': fields.many2one('res.partner', 'Conductor', required=True),
    }
    

class fleet_vehicle_log_services(osv.Model):

    _inherit = ['fleet.vehicle.log.services']
    _name = 'fleet.vehicle.log.services'

    def _get_odometer(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids, False)
        for record in self.browse(cr,uid,ids,context=context):
            if record.odometer_id:
                res[record.id] = record.odometer_id.value
        return res
      
    def _set_odometer(self, cr, uid, id, name, value, args=None, context=None):
        if not value:
            raise except_orm(_('Operation not allowed!'), _('Emptying the odometer value of a vehicle is not allowed.'))
        date = self.browse(cr, uid, id, context=context).date
        if not(date):
            date = fields.date.context_today(self, cr, uid, context=context)
        data_aux = self.browse(cr, uid, id, context=context)       
        data = {'value': value, 'date': date, 'vehicle_id': data_aux.vehicle_id.id, 'driver_id': data_aux.purchaser_id.id}
        return self.pool.get('fleet.vehicle.odometer').create(cr, uid, data, context=context)
        #return self.write(cr, uid, id, {'odometer_id': odometer_id}, context=context)
        
    _columns = {
        'odometer': fields.function(_get_odometer, fnct_inv=_set_odometer, type='float', string='Odometer Value', help='Odometer measure of the vehicle at the moment of this log'),
        }    