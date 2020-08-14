odoo.define('barcode_scanner_trading.sound_barcode_scanner_trading', function (require) {
"use strict";



var ajax = require('web.ajax');
var core = require('web.core');
var Dialog = require('web.Dialog');
var CrashManager = require('web.CrashManager').CrashManager;
var AbstractWebClient = require('web.AbstractWebClient');


var WarningDialog  = require('web.CrashManager').WarningDialog;
var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;
var qweb = core.qweb;




var CrashManager = CrashManager.include({
	

    show_warning: function (error, options) {
    	

		/****************************************************************
		 * prixgen custom code start here
		 * BARCODE_SCANNER_TRADING_ is a code to identi
		 * fy that message is coming from barcode scanner.
		 * here we remove code for display valid message and play sound.       
		 * ***************************************************************
        */
		if (error.data.message.length){
			
    		//for auto close popup start here
    		var auto_close_ms = error.data.message.match("AUTO_CLOSE_AFTER_(.*)_MS&");
    		if(auto_close_ms && auto_close_ms.length == 2){
    			auto_close_ms = auto_close_ms[1];    			
    			var original_msg = "AUTO_CLOSE_AFTER_"+ auto_close_ms +"_MS&";
    			error.data.message = error.data.message.replace(original_msg, "");  
    			setTimeout(function(){     				
    				$('.o_technical_modal').find('button[type="button"] > span:contains("Ok")').closest('button').trigger( "click" );
    			}, auto_close_ms);	    			
    			
    		} 	  
    		//for auto close popup ends here
    		
    		
    		//for play sound start here
    		//if message has BARCODE_SCANNER_TRADING_
    		var str_msg = error.data.message.match("BARCODE_SCANNER_TRADING_");    		
    		if (str_msg){
    			//remove BARCODE_SCANNER_TRADING_ from message and make valid message
    			error.data.message = error.data.message.replace("BARCODE_SCANNER_TRADING_", "");
    			    			
    			//play sound
    			var src = "/barcode_scanner_trading/static/src/sounds/error.wav";
    	        $('body').append('<audio src="'+src+'" autoplay="true"></audio>');	   
    		}
    		//for play sound ends here

		}
		
	
					
		//prixgen custom code ends here    	
    	
    	
        return this._super.apply(this, arguments);

        
    },	
	

});

return {
    CrashManager: CrashManager,
};

});


