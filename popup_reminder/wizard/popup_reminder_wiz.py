# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import osv, fields

from datetime import datetime
from tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _

class popup_reminder_wiz(osv.osv_memory):
    
    _name = 'popup.reminder.wiz'
    
    _description = 'Pop up Reminder Wizard'
    
    _columns = {        
        'alarm_id': fields.many2one('res.alarm', 'Basic Alarm',),
        }
    
    _defaults = {
        'alarm_id': 5,
       }
    
    def create_reminder(self, cr, uid, ids, context=None):

        if context and 'active_model' in context:
            name_object = context['active_model']
        if context and 'default_date' in context:
            event_date = context['default_date']
            if event_date==False:
                raise osv.except_osv(_('Warning!'), _("Enter a date for the activity."))
        if context and 'alarm_id' in context:
            alarm_id = context['alarm_id']      
            
        reminder_obj = self.pool.get('popup.reminder')
        alarm_obj = self.pool.get('res.alarm')
        crm_obj = self.pool.get(name_object)
        alarm_vals = []
        
        if alarm_id:
            alarm = alarm_obj.browse(cr, uid, alarm_id)
        else:
            raise osv.except_osv(_('Warning!'), _("Set the reminder time."))
        
        vals = {
            'trigger_duration' : alarm.trigger_duration or False,
            'name' : alarm.name or False,
            'trigger_occurs' : alarm.trigger_occurs or False, 
            'trigger_interval' : alarm.trigger_interval or False,
            'repeat' : alarm.repeat or False, 
            'trigger_related' : alarm.trigger_related or False,
            'active' : alarm.active,
            'duration' : alarm.duration or False
        }
        alarm_vals += [(0, 0, vals)]        
              
        if event_date:
            interval = alarm.trigger_interval
            duration = alarm.trigger_duration
            format_event_date = datetime.strptime(event_date,DEFAULT_SERVER_DATETIME_FORMAT)
            
            if interval == 'minutes':
                day_date = format_event_date.day
                minute_date = format_event_date.minute
                minute_decrease = minute_date - duration                
                if minute_decrease < 0:
                    hour_date = format_event_date.hour
                    if hour_date == 0:
                        alarm_date = format_event_date.replace(day=day_date-1,hour=23,minute=60+minute_decrease) 
                    else:
                        alarm_date = format_event_date.replace(hour=hour_date-1,minute=60+minute_decrease)
                else:
                    alarm_date = format_event_date.replace(minute=minute_decrease)
            if interval == 'hours':
                hour_date = format_event_date.hour
                hour_decrease = hour_date - duration
                if hour_decrease < 0:
                    day_date = format_event_date.day
                    alarm_date = format_event_date.replace(day=day_date-1,hour=24+hour_decrease)
                else:
                    alarm_date = format_event_date.replace(hour=hour_decrease)
            if interval == 'days':
                day_date = format_event_date.day
                day_decrease = day_date - duration
                alarm_date = format_event_date.replace(day=day_decrease) 
            
        crm_rec = crm_obj.browse(cr, uid, context.get('active_id', False), context=context)
        reminder_vals = {
             'name' : crm_rec.name,
             'alarm_date' : alarm_date or False,
             'event_date' : event_date or False,
             'model_id' : name_object+',' + str(context.get('active_id', False)),
             #'alarm_ids' : alarm_vals,           
        }
        reminder_id = reminder_obj.create(cr, uid, reminder_vals, context=context)
               
        return {'type': 'ir.actions.act_window_close'}
    
popup_reminder_wiz()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: