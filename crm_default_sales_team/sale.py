from osv import fields,osv

class sale_order(osv.osv):
    _inherit='sale.order'
    
    def _get_user_default_sales_team(self, cr, uid, ids, context={}):
        user= self.pool.get('res.users').browse(cr,uid,uid)
        sale_team_id=user.default_section_id.id
        return sale_team_id or False
    
    _defaults = {
                 'section_id': _get_user_default_sales_team,
                 }
    
sale_order()