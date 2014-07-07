openerp.popup_reminder = function(instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;
    instance.web.ActionManager.include({
        start: function(){
            this._super.apply(this, arguments);
            if (instance.session.session_is_valid()){
                this.alarm_popup()
            }
        },
        alarm_popup: function(){
            var self = this
            action_obj = new instance.web.ActionManager(this)
            self.alarm_obj = new instance.web.DataSetSearch(this, 'popup.reminder', {}, []);
            self.alarm_obj.call("open_alaram_popup", []).then(function(call_back){
            	console.log(call_back )
            	if(call_back && call_back.ids.length > 0){
		                self.new_alarm_dialog = $(QWeb.render('alarm_popup', {'widget': call_back})).dialog({
		                    resizable: false,
		                    width:700,
		                    modal: true,
		                    title: "Event Reminder",
		                    buttons: {
		                        "Close": function() {
		                			this.remove()
		                			$( this ).dialog( "close" );
		                		      setTimeout(function(){
		                		            self.alarm_popup()
		                		      },60000);
		                        },
		                    },
		                });
	            	
	            	self.new_alarm_dialog.find(".go_button").click(function(event){
	            		var model = this.id.split("_")[0]
	            		var res_id = parseInt(this.id.split("_")[1])
	                    return new instance.web.Model("ir.actions.act_window").get_func("search_read")([['res_model', '=', model]], ['id']).pipe(
	                            _.bind(function(res) {
	                        return instance.session.rpc('/web/action/load', {'action_id': res[0]['id']}).pipe(_.bind(function(result) {
	                            var action = result;
	                            action.domain = [['id','in',[res_id]]]
	                            action.context = {}
	                            //self.destroy();
	                            action.res_id = res_id
	                            instance.client.action_manager.do_action(action);
	                            self.new_alarm_dialog.remove()
	                  	      setTimeout(function(){
	              	            self.alarm_popup()
	                  	      },60000);
	                        }, this));
	                    }, this));
	            	})
	            	self.new_alarm_dialog.find(".accept_button").click(function(event){
	            		var res_id = parseInt(this.id)
	            		var button = this
	                	self.alarm_obj.call("accept_reminder", [[res_id]]).then(function(){
	                		console.log($(button))
	                		$(button).attr("disabled","disabled")
	                		$(button).addClass("click_button")
	                	})
	            	})
            	}else{
            	      setTimeout(function(){
            	            self.alarm_popup()
            	      },60000);
            	}
          });
        },
    });
}
