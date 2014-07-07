from openerp.osv import fields, osv
from openerp.tools.translate import _

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _columns = {
        'metting_ids': fields.one2many('crm.meeting', 'opportunity_id', 'Crm Meeting'),
        'phone_ids':fields.one2many('crm.phonecall', 'opportunity_id', 'Phonecall'),
    }

crm_lead()

class crm_meeting(osv.Model):
    """ Model for CRM meetings """
    _inherit = 'crm.meeting'
    def create(self, cr, uid, data, context=None):
        if context:
            if context.get('default_opportunity_id'):
                crm_lead_obj=self.pool.get('crm.lead')
                message = _("<b>Meetings planned </b> for the <em>%s</em>, subject: <em>%s</em>" % (data['date'],data['name']))
                crm_lead_obj.message_post(cr, uid, [context.get('default_opportunity_id')], body=message, context=context)
        return super(crm_meeting, self).create(cr, uid, data, context)
   # def default_get(self):
crm_meeting()