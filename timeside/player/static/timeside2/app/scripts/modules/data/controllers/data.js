define([
  '#qt_core/controllers/all'
],

function (A) {
  'use strict';

  return Marionette.Controller.extend({
    initialize: function (options)	 {
      /*A.vent.on(A.Cfg.events.livraison.transporteur.get,this.onGetTransporteurData,this);*/

        A._v.onCfg('data.items.get','',this.onGetItems,this);
    },

    onDestroy : function() {
      /*A.vent.off(A.Cfg.events.livraison.transporteur.get,this.onGetTransporteurData,this);*/


        A._v.offCfg('data.items.get','',this.onGetItems,this);
     
    },

    /////////////////////////////////////////////////////////////////////
    // Get Items

    onGetItems:function() {
       A.ApiEventsHelper.listenOkErrorAndTrigger3(A.Cfg.eventApi(A.Cfg.events.data.items.get),null,null,
        function(result) {
          //alert('oui');
          A._i.setOnCfg('allItems',result);
          return A.vent.trigger(A.Cfg.eventOk(A.Cfg.events.data.items.get));
        }, function(error) {
          alert("Non1");
      });
    }

  

   

  });
});
