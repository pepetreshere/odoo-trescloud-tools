# -*- coding: utf-8 -*-
########################################################################
#                                                                       
# @authors: Carlos Yumbillo                                                                          
# Copyright (C) 2013 TRESCLOUD Cia.Ltda                                   
#                                                                       
#This program is free software: you can redistribute it and/or modify   
#it under the terms of the GNU General Public License as published by   
#the Free Software Foundation, either version 3 of the License, or      
#(at your option) any later version.                                    
#
# This module is GPLv3 or newer and incompatible
# with OpenERP SA "AGPL + Private Use License"!
#                                                                       
#This program is distributed in the hope that it will be useful,        
#but WITHOUT ANY WARRANTY; without even the implied warranty of         
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
#GNU General Public License for more details.                           
#                                                                       
#You should have received a copy of the GNU General Public License      
#along with this program.  If not, see http://www.gnu.org/licenses.
#ice
########################################################################
{
   "name" : "Módulo para agregar recordatorios en iniciativas y llamadas.",
   "author" : "TRESCloud Cia. Ltda.",
   "maintainer": 'TRESCloud Cia. Ltda.',
   "website": 'http://www.trescloud.com',
   'complexity': "easy",
   "description": """
   
   Este sistema permite agregar un botón para crear recordatorios en iniciativas y llamadas.
     
   Desarrollador:
   
   Carlos Yumbillo
   
   """,
   "category": "Reminders",
   "version" : "1.0",
   'depends': ['base','crm','base_calendar','popup_reminder',],
   'init_xml': [],
   'update_xml': ['view/trescloud_leads_popup_reminder.xml',
                  'view/trescloud_calls_popup_reminder.xml',
                  'view/trescloud_meeting_popup_reminder.xml',
                  'view/trescloud_opportunity_to_call_popup_reminder.xml',],
   'installable': True,
}